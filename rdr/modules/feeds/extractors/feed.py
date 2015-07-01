# encoding: utf-8

from rdr.components.feedengine import parser

from rdr.components.helpers import http
from rdr.modules.files.images import ImageStorage
from rdr.application import app
from .article import FeedArticleExtractor


def retrieve_feed_image(src):
    remote_file = http.retrieve_remote_file(src)
    try:
        storage = ImageStorage(remote_file.open(), 'feed-icons')
        if storage.in_format(app.config['IMAGE_UPLOAD_ALLOWED_EXTENSIONS']):
            model = storage.save()
            storage.copy().fit(120, 120).save_thumbnail('package-icon')
            storage.copy().fit(16, 16).save_thumbnail('small-package-icon')
            return model
    finally:
        remote_file.remove()
    return None


class FeedExtractor(object):

    def __init__(self, feed_url, **kwargs):
        self.articles_limit = 100
        if 'articles_limit' in kwargs:
            self.articles_limit = kwargs.pop('articles_limit')
        if 'user_agent' not in kwargs:
            kwargs['user_agent'] = app.config.get('DEFAULT_USER_AGENT')
        self.parse_params = kwargs
        self.feed_url = feed_url
        self.feed = None
        self._modified = True

    @property
    def url(self):
        return self.feed.url

    @property
    def channel_url(self):
        return self.feed.channel_url

    @property
    def language(self):
        return self.feed.language

    @property
    def title(self):
        return self.feed.title

    @property
    def articles(self):
        entries = self.feed.entries
        if self.articles_limit != -1:
            entries = entries[:self.articles_limit]
        for entry in entries:
            article = FeedArticleExtractor(entry)
            if article.is_valid():
                yield article

    @property
    def image_url(self):
        return self.feed.image_url

    @property
    def http_status(self):
        return self.feed.response.http_status

    @property
    def etag_header(self):
        return self.feed.response.etag

    @property
    def modified_header(self):
        return self.feed.response.modified

    @property
    def is_modified(self):
        return self._modified

    def parse(self, **kwargs):
        kwargs.update(self.parse_params)
        feed = parser.parse(self.feed_url, **kwargs)
        if feed is None:
            self._modified = False
        self.feed = feed

    def retrieve_image(self):
        if self.image_url:
            return retrieve_feed_image(self.image_url)


class InvalidFeedException(Exception):
    pass