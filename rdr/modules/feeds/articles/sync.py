# encoding: utf-8

from datetime import datetime as DateTime
from time import mktime

from rdr.modules.feeds.extractors.feed import FeedExtractor
from rdr.application import app
from rdr.application.database import db
from rdr.modules.feeds.models import Article
from rdr.components.helpers import html, http


class ArticlesSynchronizer(object):

    def __init__(self, feed, add_to_search_index=True):
        self.feed = feed
        self.is_add_to_search_index = add_to_search_index

    def sync(self):
        feed = self.feed
        extractor = FeedExtractor(feed.channel_url)
        extractor.parse(etag=feed.last_etag_header, modified=feed.last_modified_header)
        article_models = []
        if extractor.is_modified:
            for article in extractor.articles:
                try:
                    if article.published_date:
                        from rdr.components.timezone import convert_to_local
                        published_date = convert_to_local(article.published_date)
                    else:
                        raise Exception('Empty published date')
                    if feed.last_update and published_date < feed.last_update:
                        continue
                    text = article.safe_text
                    title = article.title
                    import hashlib
                    s1 = hashlib.sha1()
                    check_string = (title + ' | ' + published_date.strftime('%Y-%m-%d %H:%M:%S')) \
                        .encode('utf-8')
                    s1.update(check_string)
                    hash_ = s1.hexdigest()
                    saved_article = Article.query.filter((Article.feed_id == feed.id) & (Article.hash == hash_)).first()
                    if saved_article is not None:
                        continue
                    fetched_date = DateTime.now()
                    article_model = Article(title=article.title,
                                            article_url=article.url,
                                            feed_id=feed.id,
                                            preview_text=html.nl2br(text),
                                            active=True,
                                            published=published_date,
                                            fetched=fetched_date,
                                            hash=hash_)
                    image_url = article.primary_image_url
                    if image_url:
                        if http.check_is_not_local_url(image_url) and http.check_is_absolute_url(image_url):
                            article_model.preview_image_src = image_url
                    article_models.append(article_model)
                    db.session.add(article_model)
                    db.session.commit()
                    if self.is_add_to_search_index:
                        from rdr.modules.feeds.search import ArticleSearchIndex
                        search_provider = ArticleSearchIndex(article_model)
                        search_provider.create_index()
                except Exception as e:
                    app.logger.exception(e)

            if not feed.active:
                feed.active = True
            feed.last_etag_header = extractor.etag_header
            feed.last_modified_header = extractor.modified_header
            feed.last_update = DateTime.now()
            db.session.commit()

        return article_models




