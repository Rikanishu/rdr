# encoding: utf-8

from rdr.application.database import db, modelrepr


class Subscribe(db.Model):

    TYPE_FOLDER = 'folder'
    TYPE_FEED = 'feed'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    parent_id = db.Column(db.Integer, index=True)
    name = db.Column(db.String(255), index=True)
    type = db.Column(db.String(32), index=True)
    order = db.Column(db.Integer)
    active = db.Column(db.Boolean, index=True)
    feed_id = db.Column(db.Integer, db.ForeignKey('feed.id', ondelete='CASCADE'))

    @property
    def feed(self):
        from rdr.modules.feeds.models import Feed
        return Feed.query.filter(Feed.id == self.feed_id).first()

    @classmethod
    def is_subscribed_on_feed(cls, user, feed):
        return cls.query.filter((cls.user_id == user.id) & (cls.feed_id == feed.id)).count() > 0

    def to_dict(self):
        result = {
            'id': self.id,
            'subscribeId': self.id,
            'authorId': self.user_id,
            'parentId': self.parent_id,
            'name': self.name,
            'type': self.type,
            'order': self.order,
            'active': self.active,
            'feedId': self.feed_id
        }
        if self.type == Subscribe.TYPE_FEED and self.feed:
            result['iconSrc'] = self.feed.small_icon_src
        return result


    def __repr__(self):
        return modelrepr('<Subscribe [%s] "%s">', self.id, self.name)
