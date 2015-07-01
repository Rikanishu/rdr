# encoding: utf-8

from __future__ import absolute_import

from . import FullTextProvider
from .newspaper import NewspaperProvider
from .diffbot import DiffBotProvider


class SmartProvider(FullTextProvider):

    def fetch_article_full_text(self, article):
        feed = article.feed
        if not feed:
            raise Exception('Can\'t fetch full text for article without feed')
        if not feed.language:
            provider = DiffBotProvider()
        else:
            provider = NewspaperProvider()
        return provider.fetch_article_full_text(article)