# encoding: utf-8

from rdr.application import app
from flask.ext.cache import Cache

cache = Cache(app)