# encoding: utf-8

IMAGE_MIMES = ['image/gif', 'image/png', 'image/jpeg']


class FeedArticleExtractor(object):

    def __init__(self, entry):
        self.entry = entry

    @property
    def title(self):
        return self.entry.title

    @property
    def summary(self):
        return self.entry.summary

    @property
    def url(self):
        return self.entry.url

    @property
    def published_date(self):
        return self.entry.published_date

    @property
    def safe_text(self, clean_stages=None):
        from bleach import clean
        if clean_stages is None:
            clean_stages = [
                {
                    'tags': ['a'],
                    'attributes': ['href', 'title'],
                    'strip': True
                }
            ]
        text = self.summary
        for stage in clean_stages:
            text = clean(text, **stage)
        return text

    @property
    def primary_image_url(self):
        # todo: get image from text
        for lnk in self.entry.links:
            if lnk.type in IMAGE_MIMES:
                return lnk.href

    def is_valid(self):
        return True
