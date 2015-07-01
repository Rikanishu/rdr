# encoding: utf-8

import re
from urlparse import urlparse, urlsplit, urlunsplit
import urllib
import requests
from rdr.components.helpers.http.file import TemporaryRemoteContent

URL_REGEXP = re.compile(
    r'^(?:http)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

LOCAL_HOSTNAME_REGEXP = re.compile(
    r'^(127\.[\d.]+|[0:]+1|localhost)$',
    re.IGNORECASE
)


def check_is_url(url):
    return re.match(URL_REGEXP, url) is not None


def check_is_not_local_url(url):
    parsed_url = urlparse(url)
    host = parsed_url.hostname
    return re.match(LOCAL_HOSTNAME_REGEXP, host) is None


def check_is_absolute_url(url):
    return bool(urlparse(url).netloc)


def encode_url(url):
    p = urlsplit(url)
    return urlunsplit(
        (p.scheme, urllib.quote(p.netloc.encode('utf-8')), urllib.quote(p.path.encode('utf-8')),
         urllib.quote(p.query.encode('utf-8')), urllib.quote(p.fragment.encode('utf-8')))
    )


def retrieve_remote_file(url, req_params=None):
    """
    Retrieve a remote file into local temporary created file

    @type url: basestring
    @rtype: rdr.components.helpers.http.file.AbstractRemoteResponse
    """
    if url and check_is_url(url) and check_is_not_local_url(url):
        if req_params is None:
            req_params = {}
        if 'verify' not in req_params:
            req_params['verify'] = False
        response = requests.get(encode_url(url), **req_params)
        if response and response.content:
            return TemporaryRemoteContent(response.content)
    raise Exception('Invalid remote file URL')