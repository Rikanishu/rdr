# encoding: utf-8

from urlparse import urljoin


class _MissedItem(object):
    pass


_missed_item = _MissedItem()


class lazyproperty(object):

    def __init__(self, func, name=None, doc=None):
        self.__name__ = name or func.__name__
        self.__module__ = func.__module__
        self.__doc__ = doc or func.__doc__
        self.func = func

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        value = obj.__dict__.get(self.__name__, _missed_item)
        if value is _missed_item:
            value = self.func(obj)
            obj.__dict__[self.__name__] = value

        return value


def prepare_relative_url(url, source_url=None):
    if source_url is not None:
        proper_url = urljoin(source_url, url)
    else:
        proper_url = url
    return proper_url