# encoding: utf-8

from rdr.application.database import db, ReprMixin
from rdr.modules.subscribes.models import Subscribe
from rdr.components.date import relative_date_format
from rdr.application.i18n import format_datetime


class Feed(db.Model, ReprMixin):

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(4096))
    channel_url = db.Column(db.String(4096), index=True)
    icon_image_id = db.Column(db.Integer, db.ForeignKey('image.id'))
    category = db.Column(db.Integer, nullable=True)
    title = db.Column(db.String(255))
    language = db.Column(db.String(12), nullable=True)
    active = db.Column(db.Boolean, index=True)
    created = db.Column(db.DateTime, index=True)
    last_update = db.Column(db.DateTime, index=True)
    last_etag_header = db.Column(db.String(255))
    last_modified_header = db.Column(db.String(255))

    feed_icon = db.relationship('Image', uselist=False)

    _subscribed_count = None

    def repr(self):
        return '<Feed [%s] "%s">', self.id, self.title

    @property
    def icon_src(self):
        """
        120x80 Icon
        """
        if self.feed_icon:
            return self.feed_icon.src('package-icon')
        return '/static/img/feeds/book-120x120.png'

    @property
    def small_icon_src(self):
        """
        16x16 Icon
        """
        if self.feed_icon:
            return self.feed_icon.src('small-package-icon')
        return '/static/img/feeds/bookmark-16x16.png'

    @property
    def subscribed_count(self):
        if not self.active:
            return 0
        if self._subscribed_count is None:
            self._subscribed_count = Subscribe.query.filter(
                (Subscribe.type == 'feed') & (Subscribe.feed_id == self.id)
            ).count()
        return self._subscribed_count

    def to_dict(self):
        return {
            'id': self.id,
            'type': 'feed',
            'title': self.title,
            'url': self.url,
            'language': self.language,
            'iconSrc': self.icon_src,
            'smallIconSrc': self.small_icon_src,
            'shortDescription': '',
            'subscribedCount': self.subscribed_count
        }


class FeedAliasKeyword(db.Model, ReprMixin):

    id = db.Column(db.Integer, primary_key=True)
    feed_id = db.Column(db.Integer, db.ForeignKey('feed.id', ondelete='CASCADE'))
    keyword = db.Column(db.String(4096), index=True)

    feed = db.relationship('Feed', lazy='select')

    def repr(self):
        return '<FeedAliasKeyword [%s] "%s">', self.feed_id, self.keyword


class FeedAliasUrl(db.Model, ReprMixin):

    id = db.Column(db.Integer, primary_key=True)
    feed_id = db.Column(db.Integer, db.ForeignKey('feed.id', ondelete='CASCADE'))
    url = db.Column(db.String(4096), index=True)

    feed = db.relationship('Feed', lazy='select')

    def repr(self):
        return '<FeedAliasUrl [%s] "%s">', self.feed_id, self.url


class Article(db.Model, ReprMixin):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(2048))
    article_url = db.Column(db.String(4096), index=True)
    feed_id = db.Column(db.Integer, db.ForeignKey('feed.id', ondelete='CASCADE'))
    preview_text = db.Column(db.Text)
    preview_image_src = db.Column(db.String(4096))
    active = db.Column(db.Boolean, index=True)
    published = db.Column(db.DateTime, index=True)
    fetched = db.Column(db.DateTime, index=True)
    hash = db.Column(db.String(64), index=True)

    full_text = db.relationship('ArticleFullText', backref='article', uselist=False, lazy='select')
    feed = db.relationship('Feed', lazy='select')

    _views_count = None
    _favorites_count = None

    @property
    def views_count(self):
        if self._views_count is None:
            count = ArticleStatus.query \
                .filter((ArticleStatus.article_id == self.id) &
                        (ArticleStatus.status == ArticleStatus.STATUS_READ)) \
                .count()
            self._views_count = int(count)
        return self._views_count

    @property
    def favorites_count(self):
        if self._favorites_count is None:
            count = ArticleFavorite.query \
                .filter((ArticleFavorite.article_id == self.id)) \
                .count()
            self._favorites_count = int(count)
        return self._favorites_count

    def repr(self):
        return '<Article [%s] "%s">', self.id, self.title

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'link': self.article_url,
            'text': self.preview_text,
            'date': format_datetime(self.published, 'dd MMM yyyy HH:mm'),
            'elapsedDate': relative_date_format(self.published),
            'imageUrl': self.preview_image_src,
            'viewsCount': self.views_count,
            'favoritesCount': self.favorites_count
        }


class ArticleFullText(db.Model, ReprMixin):

    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id', ondelete='CASCADE'))
    text = db.Column(db.Text)
    image_src = db.Column(db.String(4096))

    def repr(self):
        return '<ArticleFullText [%s] Article: %s>', self.id, self.article_id

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'imageUrl': self.image_src
        }


class ArticleStatus(db.Model, ReprMixin):

    STATUS_UNREAD = 0
    STATUS_READ = 1

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    article_id = db.Column(db.Integer, db.ForeignKey('article.id', ondelete='CASCADE'))
    status = db.Column(db.Integer, index=True)
    read_date = db.Column(db.DateTime, index=True)

    article = db.relationship('Article', backref='statuses', uselist=False)

    def repr(self):
        return '<ArticleStatus User: %s, Article: %s, Status: %s>', self.user_id, self.article_id, self.status


class ArticleFavorite(db.Model, ReprMixin):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    article_id = db.Column(db.Integer, db.ForeignKey('article.id', ondelete='CASCADE'))
    fav_date = db.Column(db.DateTime, index=True)

    article = db.relationship('Article', uselist=False)
    user = db.relationship('User', uselist=False)

    def repr(self):
        return '<ArticleFavorite User: %s, ArticleId: %s>', self.user_id, self.article_id


class ArticleTag(db.Model, ReprMixin):

    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id', ondelete='CASCADE'))
    tag = db.Column(db.String(255))

    def repr(self):
        return '<Article Tag: %s, ArticleId: %s>', self.tag, self.article_id


class OfflineReadQueue(db.Model, ReprMixin):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    article_id = db.Column(db.Integer, db.ForeignKey('article.id', ondelete='CASCADE'))
    add_date = db.Column(db.DateTime, index=True)

    article = db.relationship('Article', uselist=False)
    user = db.relationship('User', uselist=False)

    def repr(self):
        return '<OfflineReadQueue User: %s, ArticleId: %s>', self.user_id, self.article_id

class OfflineReadQueueTask(db.Model, ReprMixin):

    STATUS_STARTED = 1
    STATUS_FILE_GENERATED = 2
    STATUS_DONE = 3
    STATUS_REJECTED = 4

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    status = db.Column(db.Integer)
    out_file = db.Column(db.String(512))
    file_format = db.Column(db.String(24))

    user = db.relationship('User', uselist=False)

    def repr(self):
        return '<OfflineReadQueueTask Id: %s>', self.id

