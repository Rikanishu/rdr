# encoding: utf-8

from collections import OrderedDict
from datetime import datetime, timedelta

from rdr.application.database import db
from rdr.modules.users.session import user_session

from rdr.application.i18n import gettext


class StatsGenerator(object):

    DATES_LAST_MONTH = 1
    DATES_LAST_WEEK = 2

    def __init__(self, user=None, folder=None, dates=None, tables_limit=10):
        if user is None:
            if not user_session.is_auth:
                raise Exception('User is not authorised')
            user = user_session.identity
        self.user = user
        self.folder = folder
        if dates is None:
            dates = StatsGenerator.DATES_LAST_MONTH
        self.dates = dates
        self.tables_limit = tables_limit

    def generate_stats(self):
        feed_ids = self._get_feed_ids()
        from rdr.modules.feeds.models import Article
        articles = Article.query.filter((Article.feed_id.in_(feed_ids)))
        if self.dates == StatsGenerator.DATES_LAST_WEEK:
            days_count = 7
        elif self.dates == StatsGenerator.DATES_LAST_MONTH:
            days_count = 30
        else:
            raise Exception('Unknown date format')
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_count)
        articles = articles.filter((Article.published >= start_date) & (Article.published <= end_date))
        stats = {}
        dates = OrderedDict()
        days_of_week = self._get_days_of_week()
        for day in days_of_week:
            dates[day] = {
                'count': 0,
                'read': 0,
                'articles': []

            }
        articles = articles.all()
        for article in articles:
            if article.published:
                date = article.published.strftime('%a')
                if date in dates:
                    dates[date]['count'] += 1
                    dates[date]['articles'].append(article.id)
        from rdr.modules.feeds.models import ArticleStatus
        graph = []
        for (day, dat) in dates.items():
            articles_for_date = dat['articles']
            del dat['articles']
            if dat['count'] > 0:
                count = ArticleStatus.query.filter((ArticleStatus.user_id == self.user.id) &
                                                   (ArticleStatus.article_id.in_(articles_for_date)) &
                                                   (ArticleStatus.status == ArticleStatus.STATUS_READ)).count()
                dat['read'] = int(count)
            day = gettext(day)
            graph.append([day, dat['count'], dat['read']])
        stats['graph'] = graph

        # fetch read table date
        from rdr.modules.feeds.models import Feed

        reading_stats = db.session.query(Feed, db.func.count(ArticleStatus.id).label('total')) \
            .join(ArticleStatus.article) \
            .join(Article.feed) \
            .group_by(Feed.id) \
            .filter((ArticleStatus.status == ArticleStatus.STATUS_READ) &
                    (ArticleStatus.user_id == self.user.id) &
                    (ArticleStatus.read_date >= start_date) &
                    (ArticleStatus.read_date <= end_date)) \
            .order_by(db.desc('total')).limit(self.tables_limit)

        reading_table = []
        for (feed, count) in reading_stats:
            overall_count = Article.query.filter((Article.feed_id == feed.id) &
                                                 (Article.fetched >= start_date) &
                                                 (Article.fetched <= end_date)).count()
            if overall_count > 0:
                read_percent = (float(count) * 100) / overall_count
                if read_percent > 100:
                    read_percent = 100
                read_percent = ('%.2f' % read_percent).rstrip('0').rstrip('.')
            else:
                read_percent = '-'
            reading_table.append({
                'id': feed.id,
                'title': feed.title,
                'icon': feed.small_icon_src,
                'read_count': int(count),
                'all_count': int(overall_count),
                'read_percent': read_percent
            })
        stats['readingTable'] = reading_table

        # fetch subscriptions table data
        overall_stats = db.session.query(Feed, db.func.count(Article.id).label('total')) \
                            .join(Article.feed) \
                            .group_by(Feed.id) \
                            .filter((Article.fetched >= start_date) &
                                    (Article.fetched <= end_date) &
                                    (Article.feed_id.in_(feed_ids))) \
                            .order_by(db.desc('total')).limit(self.tables_limit)
        overall_table = []
        for (feed, count) in overall_stats:
            read_count = ArticleStatus.query.join(ArticleStatus.article) \
                    .filter((ArticleStatus.user_id == self.user.id) &
                            (ArticleStatus.status == ArticleStatus.STATUS_READ) &
                            (Article.feed_id == feed.id) &
                            (ArticleStatus.read_date >= start_date) &
                            (ArticleStatus.read_date <= end_date)).count()
            read_percent = (float(read_count) * 100) / count
            if read_percent > 100:
                read_percent = 100
            read_percent = ('%.2f' % read_percent).rstrip('0').rstrip('.')
            if read_percent == '0':
                read_percent = '-'
            overall_table.append({
                'id': feed.id,
                'title': feed.title,
                'icon': feed.small_icon_src,
                'published_count': int(count),
                'items_per_day':  ('%.2f' % (float(count) / days_count)).rstrip('0').rstrip('.'),
                'read_count': int(read_count),
                'read_percent': read_percent
            })
        stats['subscriptionsTable'] = overall_table

        read_count = ArticleStatus.query.filter((ArticleStatus.user_id == self.user.id) &
                                                (ArticleStatus.status == ArticleStatus.STATUS_READ)) \
                        .join(ArticleStatus.article) \
                        .filter((Article.feed_id.in_(feed_ids) &
                                 (ArticleStatus.read_date >= start_date) &
                                 (ArticleStatus.read_date <= end_date))).count()

        from rdr.modules.feeds.models import ArticleFavorite
        fav_count = ArticleFavorite.query.join(ArticleFavorite.article) \
                                        .filter((ArticleFavorite.user_id == self.user.id) &
                                               (Article.feed_id.in_(feed_ids)) &
                                                (ArticleFavorite.fav_date >= start_date) &
                                                (ArticleFavorite.fav_date <= end_date)).count()

        stats['subscriptionsCount'] = len(feed_ids)
        stats['publishedCount'] = len(articles)
        stats['readCount'] = read_count
        stats['favCount'] = fav_count

        return stats

    def _get_days_of_week(self):
        return [
            'Mon',
            'Tue',
            'Wed',
            'Thu',
            'Fri',
            'Sat',
            'Sun'
        ]

    def _get_feed_ids(self):
        from rdr.modules.subscribes.models import Subscribe
        user_subscribes = Subscribe.query.filter((Subscribe.user_id == self.user.id) &
                (Subscribe.active == True) &
                (Subscribe.type == Subscribe.TYPE_FEED))
        if self.folder:
            user_subscribes = user_subscribes.filter(Subscribe.parent_id == self.folder.id)
        ids = []
        for sub in user_subscribes:
            ids.append(sub.feed_id)
        return ids



