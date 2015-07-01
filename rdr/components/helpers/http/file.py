# encoding: utf-8

import os


class AbstractRemoteResponse(object):

    def open(self):
        raise NotImplementedError()

    def content(self):
        raise NotImplementedError()

    def write(self, fpath):
        raise NotImplementedError()

    def remove(self):
        raise NotImplementedError()


class TemporaryRemoteFile(AbstractRemoteResponse):

    def __init__(self, path):
        self.path = path

    def __exit__(self, typ, val, tb):
        self.remove()

    def open(self):
        return open(self.path)

    def remove(self):
        if os.path.isfile(self.path):
            os.remove(self.path)


class TemporaryRemoteContent(AbstractRemoteResponse):

    def __init__(self, binary):
        self.content = binary

    def open(self):
        from StringIO import StringIO
        return StringIO(self.content)

    def content(self):
        return self.content()

    def remove(self):
        pass

