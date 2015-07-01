# encoding: utf-8

from rdr.modules.subscribes.models import Subscribe
from rdr.modules.feeds.models import Article, ArticleStatus
from rdr.application.database import db
from rdr.application.cache import cache
from rdr.application import app
from rdr.components.helpers.lists import unique
from datetime import datetime, timedelta
from rdr.modules.users.session import user_session


class PopularNewsGenerator(object):

    def __init__(self, user=None, articles_count=15, use_cache=True, cache_timeout=1200):
        if user is None:
            if not user_session.is_auth:
                raise Exception('User is not authorised')
            user = user_session.identity
        self.user = user
        # one hour by default
        self.timeout = cache_timeout
        self.articles_count = articles_count
        self.use_cache = use_cache

    def fetch_news(self):
        article_ids = None
        key = self._get_cache_key() + '.' + str(self.user.id)
        if self.use_cache:
            try:
                article_ids = cache.get(key)
            except Exception as e:
                app.logger.exception(e)
                app.logger.info("An exception catched, disable cache")
                self.use_cache = False
        if article_ids is None:
            article_ids = self.generate()
            if self.use_cache:
                cache.set(key, article_ids, timeout=self.timeout)
        return article_ids

    def fetch_articles(self):
        ids = self.fetch_news()
        if not ids:
            return []
        articles = Article.query.filter(Article.id.in_(ids))
        return sorted(articles.all(), key=lambda x: x.preview_image_src, reverse=True)

    def generate(self):
        date_from = self._get_date_from()
        if date_from is None:
            return []
        stats = db.session.query(ArticleStatus.article_id, db.func.count(ArticleStatus.id).label('total')) \
            .join(ArticleStatus.article) \
            .join(Subscribe, ((Subscribe.type == Subscribe.TYPE_FEED) & (Subscribe.feed_id == Article.feed_id))) \
            .group_by(ArticleStatus.article_id).filter(
                (ArticleStatus.status == ArticleStatus.STATUS_READ) &
                (Subscribe.user_id == self.user.id) &
                (Article.fetched >= date_from)
            ).order_by(db.desc('total')).limit(self.articles_count)

        article_ids = []
        for (article_id, _count) in stats:
            article_ids.append(article_id)

        article_ids = list(unique(article_ids))
        return article_ids

    def _get_date_from(self):
        last_visit_date = datetime.now() - timedelta(hours=24)
        return last_visit_date

    def _get_cache_key(self):
        return 'popular_news'

class LastVisitNewsGenerator(PopularNewsGenerator):

    def _get_date_from(self):
        if not self.user.last_visit:
            return None
        delta = datetime.now() - self.user.last_visit
        last_visit_date = datetime.now() - delta
        return last_visit_date

    def _get_cache_key(self):
        return 'latest_news'