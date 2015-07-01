# encoding: utf-8

from elasticsearch import Elasticsearch, TransportError
from . import app

es = Elasticsearch([app.config.get('ELASTIC_SEARCH_URI')])