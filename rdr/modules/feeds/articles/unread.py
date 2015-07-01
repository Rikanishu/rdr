# encoding: utf-8

from rdr.modules.feeds.models import Article, ArticleStatus, Feed
from rdr.modules.subscribes.models import Subscribe
from rdr.application.database import db


class AbstractUnreadArticlesSet(object):

    @property
    def count(self):
        """
        Return count of articles
        @rtype: int
        """
        return self.query.count()

    @property
    def articles(self):
        """
        Return article models list
        @rtype: list
        """
        return self.query.all()

    @property
    def query(self):
        """
        Return SQLAlchemy query object for set
        """
        raise NotImplementedError('Method is not implemented')


class TotalUnreadArticlesSet(AbstractUnreadArticlesSet):

    def __init__(self, user):
        self.user = user

    @property
    def query(self):
        return Article.query.join(
            Subscribe, (Subscribe.feed_id == Article.feed_id) &
                       (Subscribe.active == True) &
                       (Subscribe.user_id == self.user.id)
        ).outerjoin(
            ArticleStatus, (ArticleStatus.user_id == self.user.id) &
                           (ArticleStatus.article_id == Article.id)
        ).options(
            db.contains_eager(Article.statuses)
        ).filter((Article.active == True) & (
            (ArticleStatus.id == None) | (ArticleStatus.status == ArticleStatus.STATUS_UNREAD)
        )).order_by(Article.published.desc())


class FeedUnreadArticlesSet(TotalUnreadArticlesSet):

    def __init__(self, user, feed):
        super(FeedUnreadArticlesSet, self).__init__(user)
        assert feed is not None, "Can't get unread count for null feed"
        self.feed = feed

    @property
    def query(self):
        return Article.query.outerjoin(
            ArticleStatus, (ArticleStatus.user_id == self.user.id) &
                           (ArticleStatus.article_id == Article.id)
        ).options(
            db.contains_eager(Article.statuses)
        ).filter(
            (Article.active == True) & (Article.feed_id == self.feed.id) &
            ((ArticleStatus.id == None) | (ArticleStatus.status == ArticleStatus.STATUS_UNREAD))
        ).order_by(Article.published.desc())