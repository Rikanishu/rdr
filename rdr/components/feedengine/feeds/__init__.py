# encoding: utf-8

from lxml import etree


class UnknownFeedException(Exception):
    pass


class InvalidFormatException(Exception):
    pass


class ParseError(Exception):
    pass


class HttpResponse(object):

    def __init__(self, url='', http_status=200, etag=None, modified=None):
        self.url = url
        self.http_status = http_status
        self.etag = etag
        self.modified = modified


class Link(object):

    def __init__(self, href, rel=None, type=None, options=None):
        self.href = href
        self.rel = rel
        self.type = type
        self.options = options or {}


class Feed(object):

    def __init__(self, xml, response=None):
        self.tree = etree.fromstring(xml)
        self.resp = response
        if not self.is_valid_feed():
            raise UnknownFeedException

    def is_valid_feed(self):
        raise NotImplementedError

    @property
    def response(self):
        return self.resp

    @property
    def language(self):
        return None

    @property
    def url(self):
        raise NotImplementedError

    @property
    def channel_url(self):
        raise NotImplementedError

    @property
    def title(self):
        raise NotImplementedError

    @property
    def entries(self):
        raise NotImplementedError

    @property
    def image_url(self):
        raise NotImplementedError


class Entry(object):

    def __init__(self, element, feed):
        self.element = element
        self.feed = feed

    @property
    def title(self):
        raise NotImplementedError

    @property
    def summary(self):
        raise NotImplementedError

    @property
    def url(self):
        raise NotImplementedError

    @property
    def published_date(self):
        raise NotImplementedError

    @property
    def links(self):
        raise NotImplementedError