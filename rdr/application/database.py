# encoding: utf-8

from flask.ext.sqlalchemy import SQLAlchemy
from rdr.application import app


db = SQLAlchemy(app)


class ReprMixin(object):

    def __init__(self, *args, **kwargs):
        """
        This method is unnecessary
        It's just a hack for IDE highlighting
        """
        super(ReprMixin, self).__init__(*args, **kwargs)

    def repr(self):
        return self.__class__.__name__

    def unicoderepr(self):
        rep = self.__repr__()
        if isinstance(rep, str):
            rep = rep.decode('utf-8')
        return rep

    def __repr__(self):
        rep = self.repr()
        if isinstance(rep, tuple):
            rep = modelrepr(rep[0], *rep[1:])
        return rep

    def __unicode__(self):
        rep = self.unicoderepr()
        if isinstance(rep, tuple):
            rep = unicoderepr(rep[0], *rep[1:])
        return rep


def modelrepr(reprformat, *args):
    args = [x.encode('utf-8') if isinstance(x, unicode) else x for x in args]
    reprformat = reprformat.encode('utf-8') if isinstance(reprformat, unicode) else reprformat
    return reprformat % tuple(args)


def unicoderepr(reprformat, *args):
    args = [x.decode('utf-8') if isinstance(x, str) else x for x in args]
    reprformat = reprformat.decode('utf-8') if isinstance(reprformat, str) else reprformat
    return reprformat % tuple(args)



