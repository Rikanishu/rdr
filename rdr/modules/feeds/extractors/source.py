# encoding: utf-8

import requests
import lxml.html as lhtml
from rdr.application import app
from urlparse import urljoin

from .feed import retrieve_feed_image


def _prepare_relative_url(url, source_url=None):
    if source_url is not None:
        proper_url = urljoin(source_url, url)
    else:
        proper_url = url
    return proper_url


class SourceExtractor(object):

    def __init__(self, url, feeds_limit=5):
        self.url = url
        self.feeds_limit = feeds_limit
        self.image_url = None
        self.language = None
        self.feed_urls = []
        self.title = 'Unnamed source'

    def parse(self):
        headers = {}
        if 'DEFAULT_USER_AGENT' in app.config:
            headers['User-Agent'] = app.config.get('DEFAULT_USER_AGENT')
        res = requests.get(self.url, headers=headers)
        if res.status_code >= 400:
            raise InvalidSourceException('Source has returned error code %s' % res.status_code)
        if 'content-type' not in res.headers:
            raise InvalidSourceException('Missed content type header')
        content_type = res.headers['content-type'].split(';')[0]
        if content_type != 'text/html':
            raise InvalidSourceException('Source page content is not html')
        text = res.text
        if isinstance(text, unicode):
            text = text.encode('utf-8')
        content = lhtml.fromstring(text)
        self._fetch_image(content)
        self._fetch_feeds(content)
        self._fetch_title(content)
        self._fetch_language(content)

    def retrieve_image(self):
        if self.image_url:
            return retrieve_feed_image(self.image_url)
        return None

    def _fetch_image(self, content):
        priority = [
            ('head > link[rel="icon"][type!="image/ico"][type!="image/x-icon"]', 'href'),
            ('head > link[rel="apple-touch-icon"][sizes="120x120"]', 'href'),
            ('head > link[rel="apple-touch-icon"]', 'href'),
            ('head > link[rel="apple-touch-icon-precomposed"][sizes="120x120"]', 'href'),
            ('head > link[rel="apple-touch-icon-precomposed"]', 'href'),
            ('head > meta[name="msapplication-square150x150logo"]', 'content'),
            ('head > meta[property="og:image"]', 'content'),
        ]
        for (selector, attr_name) in priority:
            images_meta = content.cssselect(selector)
            if images_meta:
                image_elem = images_meta[0]
                attrs_dict = dict(image_elem.items())
                if attr_name in attrs_dict and attrs_dict[attr_name]:
                    self.image_url = _prepare_relative_url(attrs_dict[attr_name], self.url)
                    return

    def _fetch_feeds(self, content):
        sources = [
            'head > link[rel="alternate"][type="application/rss+xml"]',
            'head > link[rel="alternate"][type="application/rss+atom"]',
        ]
        self.feed_urls = []
        for source in sources:
            feeds = content.cssselect(source)
            if feeds:
                for url_elem in feeds:
                    attrs_dict = dict(url_elem.items())
                    if 'href' in attrs_dict:
                        self.feed_urls.append(_prepare_relative_url(attrs_dict['href'], self.url))
                        self.feed_urls = self.feed_urls[:self.feeds_limit-1]
            if self.feed_urls:
                return

    def _fetch_title(self, content):
        titles = content.cssselect('head > title')
        if titles:
            self.title = titles[0].text

    def _fetch_language(self, content):
        html = content.cssselect('html')
        if html:
            elem = html[0]
            attrs = dict(elem.items())
            self.language = attrs.get('lang')


class InvalidSourceException(Exception):
    pass