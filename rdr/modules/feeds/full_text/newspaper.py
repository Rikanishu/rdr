# encoding: utf-8

from __future__ import absolute_import

from rdr.application import app
from rdr.modules.feeds.full_text import FullTextProvider, ArticleFullTextResult
from rdr.components.helpers import http


class NewspaperProvider(FullTextProvider):

    def fetch_article_full_text(self, article):
        from newspaper import Article as NewspaperArticle
        from newspaper.utils import get_available_languages
        feed = article.feed
        if not feed:
            raise Exception('Can\'t fetch full text for article without feed')
        lang = feed.language
        supported_langs = get_available_languages()
        if not lang or lang not in supported_langs:
            app.logger.warning('%s not in newspaper languages list' % lang)
            lang = None
            if article.preview_text:
                try:
                    from langdetect import detect
                    lang = detect(article.preview_text)
                    if lang not in supported_langs:
                        lang = None
                except ImportError:
                    pass
                except Exception as e:
                    app.logger.exception(e)
            if not lang:
                lang = 'en'

        np_article = NewspaperArticle(article.article_url,
                                      language=lang,
                                      browser_user_agent=app.config.get('DEFAULT_USER_AGENT'),
                                      keep_article_html=True)
        np_article.download()
        np_article.parse()
        images = []
        top_image_url = np_article.top_image
        if top_image_url:
            if http.check_is_absolute_url(top_image_url) and http.check_is_not_local_url(top_image_url):
                images.append({
                    'src': top_image_url,
                    'primary': True
                })
        return ArticleFullTextResult(title=np_article.title,
                                     text=np_article.text,
                                     images=images)