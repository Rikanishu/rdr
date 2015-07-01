# encoding: utf-8

import requests
from rdr.components.feedengine.feeds import HttpResponse, UnknownFeedException
from rdr.components.feedengine.feeds.atom import AtomFeed
from rdr.components.feedengine.feeds.rss20 import Rss20Feed

DEFAULT_USER_AGENT = 'FeedEngine-Parser/0.1'
ACCEPT_TYPES = ','.join([
    'application/atom+xml',
    'application/rss+xml',
    'application/rdf+xml',
    'application/xml;q=0.9',
    'text/xml;q=0.2',
    '*/*;q=0.1',
    ])
FEEDS = [
    AtomFeed,
    Rss20Feed
]

class FeedFetchingException(Exception):
    pass


def parse(url, user_agent=None, modified=None, etag=None):
    headers = {}
    if user_agent is None:
        user_agent = DEFAULT_USER_AGENT
    headers['User-Agent'] = user_agent
    headers['Accept'] = ACCEPT_TYPES
    if modified:
        headers['If-Modified-Since'] = modified
    if etag:
        headers['If-None-Match'] = etag
    res = requests.get(url, headers=headers)
    if res.status_code == 304:
        if etag is not None or modified is not None:
            return None
        raise Exception('Invalid not modified response')
    if res.status_code >= 400:
        raise FeedFetchingException('Source has returned error code %s' % res.status_code)
    http_response = HttpResponse(url=res.url, http_status=res.status_code,
                                 etag=res.headers.get('ETag'), modified=res.headers.get('Last-Modified'))
    known_feed = None
    for feed in FEEDS:
        try:
            known_feed = feed(res.content, response=http_response)
            break
        except UnknownFeedException:
            pass
    if known_feed is None:
        raise UnknownFeedException('Unknown feed format')
    return known_feed




