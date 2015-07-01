# encoding: utf-8

from urlparse import urlparse

from rdr.components.feedengine.utils import lazyproperty, prepare_relative_url
from rdr.components.feedengine.feeds import Feed, Entry, Link, HttpResponse, InvalidFormatException


ATOM_MIME_TYPE = 'application/atom+xml'
HTML_MIME_TYPE = 'text/html'


def xmlnstag(tag):
    return '{http://www.w3.org/2005/Atom}' + tag


class AtomFeed(Feed):

    def is_valid_feed(self):
        return self.tree.tag == xmlnstag('feed')

    @lazyproperty
    def url(self):
        alter_links = [link for link in self.links if link.rel == 'alternate']
        if alter_links:
            for link in alter_links:
                if link.type == HTML_MIME_TYPE:
                    return link.href
            return alter_links[0].href
        return None

    @lazyproperty
    def channel_url(self):
        resp = self.http_response()
        if resp and resp.url:
            return resp.url
        self_links = [link for link in self.links if link.rel == 'self']
        if self_links:
            for link in self_links:
                if link.type == ATOM_MIME_TYPE:
                    return link.href
            return self_links[0].href
        return None

    @lazyproperty
    def title(self):
        title = self.tree.find(xmlnstag('title'))
        if title is None:
            raise InvalidFormatException('Title element is missed')
        return title.text

    @lazyproperty
    def language(self):
        return None

    @lazyproperty
    def entries(self):
        return [AtomEntry(element, self) for element in self.tree.iterchildren(tag=xmlnstag('entry'))]

    @lazyproperty
    def image_url(self):
        icon = self.tree.find(xmlnstag('icon'))
        if icon is not None:
            channel_url = self.channel_url
            parsed_url = urlparse(channel_url)
            netloc = parsed_url.netloc
            scheme = parsed_url.scheme
            if not scheme:
                scheme = 'http'
            return prepare_relative_url(icon.text, scheme + '://' + netloc)
        return None

    @lazyproperty
    def links(self):
        links = []
        for el in self.tree.iterchildren(tag=xmlnstag('link')):
            links.append(Link(el.get('href'), rel=el.get('rel'), type=el.get('type')))
        return links

    def http_response(self):
        if self.response and isinstance(self.response, HttpResponse):
            return self.response
        return None


class AtomEntry(Entry):

    @lazyproperty
    def title(self):
        title = self.element.find(xmlnstag('title'))
        if title is None:
            raise InvalidFormatException('Title entry element is missed')
        return title.text

    @lazyproperty
    def summary(self):
        summary = self.element.find(xmlnstag('summary'))
        if summary is None:
            return u''
        return summary.text

    @lazyproperty
    def url(self):
        links = self.links
        if links:
            for link in self.links:
                if link.rel == 'alternate':
                    return link.href
            return links[0].href
        return None

    @lazyproperty
    def published_date(self):
        published = self.element.find(xmlnstag('published'))
        if published is None:
            published = self.element.find(xmlnstag('updated'))
            if published is None:
                raise InvalidFormatException('Updated entry element is missed')

        from dateutil import parser

        return parser.parse(published.text)

    @lazyproperty
    def links(self):
        links = []
        for el in self.element.iterchildren(tag=xmlnstag('link')):
            links.append(Link(el.get('href'), rel=el.get('rel'), type=el.get('type')))
        return links