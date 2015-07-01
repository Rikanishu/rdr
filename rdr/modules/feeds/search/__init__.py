# encoding: utf-8

from rdr.application import app

SEARCH_IN_TEXT = 'text'
SEARCH_IN_ANNOUNCE = 'announce'
SEARCH_IN_TITLE = 'title'

FILTER_ALL = 'all'
FILTER_READ_ONLY = 'read'
FILTER_UNREAD = 'unread'
FILTER_FAV = 'fav'

if app.config.get('ELASTIC_SEARCH_ENABLED', False):
    from .engine import ElasticSearchEngine as Engine
else:
    from .engine import DatabaseSearchEngine as Engine


class ArticleSearchIndex(object):

    def __init__(self, article):
        self.article = article

    def create_index(self):
        Engine().create_index(self.article)

    def create_full_text_index(self, full_text_model):
        Engine().create_full_text_index(self.article, full_text_model)


class ArticleSearchProvider(object):

    def __init__(self, feeds=None, user=None):
        if feeds:
            self.feed_ids = feeds
        elif user:
            self.feed_ids = self._fetch_subscribed_feed_ids(user)
        else:
            self.feed_ids = None
        self.user = user

    def search(self, subject, where=None, filter_criteria=FILTER_ALL):
        if where is None:
            where = [SEARCH_IN_ANNOUNCE, SEARCH_IN_TITLE, SEARCH_IN_TEXT]
        return Engine().search(subject, where,
                               user=self.user, feed_ids=self.feed_ids,
                               filter_criteria=filter_criteria)

    def _fetch_subscribed_feed_ids(self, user):
        from rdr.modules.subscribes.models import Subscribe
        user_subscribes = Subscribe.query.filter((Subscribe.user_id == user.id) &
                                                 (Subscribe.active == True) &
                                                 (Subscribe.type == Subscribe.TYPE_FEED))
        ids = []
        for sub in user_subscribes:
            ids.append(sub.feed_id)
        return ids