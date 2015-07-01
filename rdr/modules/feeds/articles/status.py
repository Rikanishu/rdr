# encoding: utf-8

from collections import OrderedDict
from rdr.modules.feeds.models import ArticleStatus, ArticleFavorite, Feed
from rdr.modules.users.session import user_session
from rdr.modules.subscribes.models import Subscribe


def _get_identity(user):
    if user is None:
        if not user_session.is_auth:
            raise Exception("Can't wrap objects for guest user")
        return user_session.identity
    return user


class UserArticleRecord(object):

    def __init__(self, article, status=ArticleStatus.STATUS_UNREAD, is_fav=False):
        self.article = article
        self.status = status
        self.is_fav = is_fav

    def to_dict(self, feed_info=True, full_text=False):
        data = self.article.to_dict()
        data['isRead'] = (self.status == ArticleStatus.STATUS_READ)
        data['isInFavorites'] = self.is_fav
        if feed_info and self.article.feed:
            feed = UserPackageRecord.wrap_package(self.article.feed)
            data['feed'] = feed.to_dict()
        if full_text and self.article.full_text:
            data['fullText'] = self.article.full_text.text
        return data

    @classmethod
    def wrap_articles_list(cls, articles, user=None):
        if not articles:
            return []
        user = _get_identity(user)
        art_dict = OrderedDict()
        for article in articles:
            art_dict[article.id] = UserArticleRecord(article)
        statuses = ArticleStatus.query.filter((ArticleStatus.article_id.in_(art_dict.keys()) &
                                               (ArticleStatus.user_id == user.id)))
        favorites = ArticleFavorite.query.filter((ArticleFavorite.article_id.in_(art_dict.keys()) &
                                                  (ArticleFavorite.user_id == user.id)))
        for stat in statuses:
            if stat.article_id in art_dict:
                art_dict[stat.article_id].status = stat.status
        for fav in favorites:
            if fav.article_id in art_dict:
                art_dict[fav.article_id].is_fav = True

        feed_ids = []
        for article in articles:
            feed_ids.append(article.feed_id)

        return art_dict.values()


    @classmethod
    def wrap_article(cls, article, user=None):
        user = _get_identity(user)
        rec = UserArticleRecord(article)
        stat = ArticleStatus.query.filter((ArticleStatus.article_id == article.id) &
                                          (ArticleStatus.user_id == user.id)).first()
        fav = ArticleFavorite.query.filter((ArticleFavorite.article_id == article.id) &
                                           (ArticleFavorite.user_id == user.id)).first()
        if stat:
            rec.status = stat.status
        if fav:
            rec.is_fav = True

        return rec


class UserPackageRecord(object):

    def __init__(self, package, is_subscribed=False):
        self.package = package
        self.is_subscribed = is_subscribed

    def to_dict(self):
        data = self.package.to_dict()
        data['isSubscribed'] = self.is_subscribed
        return data

    @classmethod
    def wrap_packages_list(cls, packages, user=None):
        if not packages:
            return []
        user = _get_identity(user)
        pack_dict = OrderedDict()
        for feed in packages:
            pack_dict[feed.id] = UserPackageRecord(feed)
        subscribes = Subscribe.query.filter((Subscribe.feed_id.in_(pack_dict.keys()) &
                                            (Subscribe.type == Subscribe.TYPE_FEED) &
                                            (Subscribe.user_id == user.id)))
        for subscribe in subscribes:
            if subscribe.feed_id in pack_dict:
                pack_dict[subscribe.feed_id].is_subscribed = True

        return pack_dict.values()

    @classmethod
    def wrap_package(cls, package, user=None):
        user = _get_identity(user)
        rec = UserPackageRecord(package)
        subscribe = Subscribe.query.filter((Subscribe.feed_id == package.id) &
                                             (Subscribe.type == Subscribe.TYPE_FEED) &
                                             (Subscribe.user_id == user.id)).first()
        if subscribe:
            rec.is_subscribed = True

        return rec
