# encoding: utf-8

from datetime import datetime

from rdr.application import app
from rdr.application.database import db
from rdr.components.helpers import http
from rdr.components.helpers import lists
from rdr.modules.feeds.extractors.source import SourceExtractor
from rdr.modules.feeds.models import FeedAliasKeyword, FeedAliasUrl, Feed
from rdr.modules.feeds.extractors.feed import FeedExtractor, InvalidFeedException
from rdr.modules.feeds.articles.status import UserPackageRecord

from .lang import try_to_resolve_lang_by_domain


class PackagesResolver(object):

    def __init__(self, query, load_articles=False, is_channel_url=False):
        self.query = query
        self.load_articles = load_articles
        self.feeds = []
        self.is_channel_url = is_channel_url

    def run(self):
        app.logger.info('Run resolver for ("%s", LA: %s, C: %s)' %
                        (self.query, self.load_articles, self.is_channel_url))
        self.feeds = self._fetch_feeds()
        return self

    def resolve(self):
        app.logger.info('Resolve packages for ("%s", LA: %s, C: %s)' %
                        (self.query, self.load_articles, self.is_channel_url))
        self.feeds = self._resolve(self.query)
        return self

    def _fetch_feeds(self):
        if self.is_channel_url:
            return self._fetch_feeds_channel()
        else:
            return self._fetch_feeds_common()

    def _fetch_feeds_channel(self):
        query = self.query
        if self.is_url(query):
            match_feed = Feed.query.filter(Feed.channel_url == query).first()
            if match_feed:
                return [match_feed]
            match_alias = FeedAliasUrl.query.filter(FeedAliasUrl.url == query).options(
                db.joinedload(FeedAliasUrl.feed)
            ).all()
            if match_alias:
                return lists.unique([m.feed for m in match_alias])
            try:
                return self._resolve(query)
            except Exception as e:
                app.logger.exception(e)
        return []


    def _fetch_feeds_common(self):
        query = self.query
        if query and len(query) > 2:
            if self.is_url(query):
                match_feed = Feed.query.filter((Feed.url == query) | (Feed.channel_url == query)).first()
                if match_feed:
                    return [match_feed]
                match_alias = FeedAliasUrl.query.filter(FeedAliasUrl.url == query).options(
                    db.joinedload(FeedAliasUrl.feed)
                ).all()
                if match_alias:
                    return lists.unique([m.feed for m in match_alias])
                try:
                    return self._resolve(query)
                except Exception as e:
                    app.logger.exception(e)
                return []

            #todo: add active
            matches = []
            match_alias = FeedAliasKeyword.query.filter(FeedAliasKeyword.keyword.ilike('%' + query + '%')).options(
                db.joinedload(FeedAliasKeyword.feed)
            ).all()
            if match_alias:
                for alias in match_alias:
                    matches.append(alias.feed)
            feeds = Feed.query.filter(Feed.title.ilike('%' + query + '%')).all()
            if feeds:
                for feed in feeds:
                    matches.append(feed)
            return lists.unique(matches)

        return []


    def _resolve(self, query):
        query = http.encode_url(query)
        extractors = []
        ex = FeedExtractor(query)
        source = SourceExtractor(query)
        feeds = []
        try:
            source.parse()
        except Exception as e:
            app.logger.exception(e)
            source = None
        try:
            ex.parse()
            extractors.append(ex)
            if not source:
                app.logger.info('Try to extract source data via rss site url')
                source = SourceExtractor(ex.url)
                try:
                    source.parse()
                except Exception as e:
                    app.logger.exception(e)
                    source = None
        except InvalidFeedException as e:
            app.logger.exception(e)
            if not source or not source.feed_urls:
                return []
            app.logger.info('Try to get alternate RSS feeds from site url')
            for url in source.feed_urls:
                match_feed = Feed.query.filter((Feed.url == url) | (Feed.channel_url == url)).first()
                if match_feed:
                    feeds.append(match_feed)
                else:
                    # todo: multi threading parsing
                    app.logger.info('Try to extract feeds from alternate source: "%s"' % url)
                    ex = FeedExtractor(url)
                    ex.parse()
                    extractors.append(ex)
        if extractors:
            for extractor in extractors:
                lang = extractor.language
                if not lang and source:
                    lang = source.language
                if not lang:
                    lang = try_to_resolve_lang_by_domain(query)
                if lang:
                    lang = lang[:2]
                feed = Feed(url=extractor.url,
                            channel_url=extractor.channel_url,
                            title=extractor.title or 'Unnamed feed',
                            language=lang,
                            active=False,
                            created=datetime.now())
                db.session.add(feed)
                db.session.commit()
                db.session.add(FeedAliasKeyword(keyword=feed.title, feed_id=feed.id))
                if query != feed.url and query != feed.channel_url:
                    db.session.add(FeedAliasUrl(url=query, feed_id=feed.id))
                db.session.commit()
                feeds.append(feed)
                try:
                    image = None
                    if source:
                        image = source.retrieve_image()
                    if not image:
                        image = extractor.retrieve_image()
                    if image:
                        image.owner_id = None

                        db.session.add(image)
                        db.session.commit()

                        feed.icon_image_id = image.id
                        db.session.commit()
                except Exception as e:
                    app.logger.exception(e)
        if self.load_articles:
            app.logger.info('Load articles')
            # todo: multi threading loading
            for feed in feeds:
                try:
                    from rdr.modules.feeds.articles.sync import ArticlesSynchronizer
                    synchronizer = ArticlesSynchronizer(feed)
                    synchronizer.sync()
                except Exception as e:
                    app.logger.exception(e)
        return feeds

    def is_url(self, query):
        return http.check_is_url(query) and http.check_is_not_local_url(query)

    def result_feeds(self):
        return list(self.feeds)

    def result_dict(self):
        feeds = self.feeds
        res = []
        sorted_feeds = sorted((x for x in feeds if x), key=lambda x: x.subscribed_count, reverse=True)
        records = UserPackageRecord.wrap_packages_list(sorted_feeds)
        for rec in records:
            res.append(rec.to_dict())
        return res
