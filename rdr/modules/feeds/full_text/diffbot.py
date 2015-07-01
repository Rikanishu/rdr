# encoding: utf-8

import requests

from rdr.modules.feeds.full_text import FullTextProvider, ArticleFullTextResult
from rdr.application import app
from rdr.components.helpers import http


class DiffBotProvider(FullTextProvider):

    def fetch_article_full_text(self, article):
        json = self.request(article.article_url)
        if 'objects' in json:
            for obj in json['objects']:
                return ArticleFullTextResult(
                    title=obj.get('title', ''),
                    text=obj.get('text', ''),
                    images=self.fetch_images(obj)
                )
        return None

    def request(self, url):
        assert url, 'Article url is empty'
        token = app.config.get('DIFFBOT_API_TOKEN', None)
        assert token, 'DIFFBOT_API_TOKEN is required parameter for using Diffbot provider'
        api_url = app.config.get('DIFFBOT_API_URL', 'http://api.diffbot.com/v3/analyze')
        response = requests.get(api_url, params={
            'token': token,
            'url': http.encode_url(url),
            'fields': 'title,text,images'
        })
        return response.json()

    def fetch_images(self, obj):
        result = []
        if 'images' in obj:
            for img in obj['images']:
                if 'url' in img and img['url']:
                    if http.check_is_absolute_url(img['url']) and http.check_is_not_local_url(img['url']):
                        result.append({
                            'primary': img.get('primary', False),
                            'src': img['url']
                        })
        return result
