# encoding: utf-8

from rdr.components.feedengine.utils import lazyproperty
from rdr.components.feedengine.feeds import Feed, Entry, Link, HttpResponse, InvalidFormatException


class Rss20Feed(Feed):

    def is_valid_feed(self):
        return self.tree.tag == 'rss' and self.tree.get('version') == '2.0'

    @lazyproperty
    def language(self):
        lang = self.tree.find('channel/language')
        if lang is not None:
            return lang.text
        return None

    @lazyproperty
    def url(self):
        link = self.tree.find('channel/link')
        if link is None:
            raise InvalidFormatException('Channel link is missed')
        return link.text

    @lazyproperty
    def channel_url(self):
        resp = self.http_response()
        if resp and resp.url:
            return resp.url
        return None

    @lazyproperty
    def title(self):
        title = self.tree.find('channel/title')
        if title is None:
            raise InvalidFormatException('Channel title is missed')
        return title.text

    @lazyproperty
    def entries(self):
        return [Rss20Entry(element, self) for element in self.tree.find('channel').iterchildren(tag='item')]

    @lazyproperty
    def image_url(self):
        image = self.tree.find('channel/image')
        if image is not None:
            url = image.find('url')
            if url is not None:
                return url.text
        return None

    def http_response(self):
        if self.response and isinstance(self.response, HttpResponse):
            return self.response
        return None


class Rss20Entry(Entry):

    @lazyproperty
    def title(self):
        title = self.element.find('title')
        if title is None:
            raise InvalidFormatException('Entry title is missed')
        return title.text

    @lazyproperty
    def summary(self):
        summary = self.element.find('description')
        if summary is None:
            # raise InvalidFormatException('Entry summary is missed')
            return u''
        return summary.text

    @lazyproperty
    def url(self):
        link = self.element.find('link')
        if link is None:
            raise InvalidFormatException('Entry link is missed')
        return link.text

    @lazyproperty
    def published_date(self):
        date = self.element.find('pubDate')
        if date is None:
            raise InvalidFormatException('Published Date is missed')

        from dateutil import parser

        return parser.parse(date.text)

    @lazyproperty
    def links(self):
        links = []
        for el in self.element.iterchildren(tag='enclosure'):
            links.append(Link(el.get('url'), type=el.get('type'), options={
                'length': el.get('length')
            }))
        return links
