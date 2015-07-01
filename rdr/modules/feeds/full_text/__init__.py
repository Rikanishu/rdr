# encoding: utf-8

import importlib
from rdr.application import app


def escape_all(text):
    from bleach import clean
    return clean(text, tags=[], attributes=[], strip=True)


class ArticleFullTextResult(object):

    def __init__(self, title='', text='', images=None):
        self.text = text
        self.title = title,
        if images is None:
            images = []
        self.images = images

    @property
    def primary_image(self):
        if self.images:
            for img in self.images:
                if 'primary' in img and img['primary']:
                    return img['src']
            return self.images[0]['src']
        return None

    @property
    def safe_text(self):
        return escape_all(self.text)

    @property
    def safe_title(self):
        return escape_all(self.title)


class FullTextProvider(object):

    def fetch_article_full_text(self, article):
        """
        :rtype: FullTextResult
        """
        raise NotImplementedError()

    @classmethod
    def provider(cls, *args, **kwargs):
        provider_module = app.config.get('ARTICLES_FULLTEXT_PROVIDER', None)
        assert provider_module, 'Full text provider module is not defined'
        if isinstance(provider_module, (str, unicode)):
            parts = provider_module.split('.')
            mod = importlib.import_module('.'.join(parts[:-1]))
            mod_cls = getattr(mod, parts[-1], None)
            assert provider_module and mod_cls, 'Full text provider class is not defined'
            return mod_cls(*args, **kwargs)
        return provider_module(*args, **kwargs)
