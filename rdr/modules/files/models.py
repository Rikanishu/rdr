# encoding: utf-8

from rdr.application.database import db, ReprMixin


class Image(db.Model, ReprMixin):

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    name = db.Column(db.String(255), default='')
    extension = db.Column(db.String(255), default='')
    path = db.Column(db.String(1024), default='')

    owner = db.relationship('User', uselist=False, foreign_keys=[owner_id], post_update=True)

    def repr(self):
        return '<Image [%s] "%s.%s">', self.id, self.name, self.extension

    def src(self, thumbnail_name=None):
        filename = self.name
        if thumbnail_name is not None:
            filename = self.name + '-' + thumbnail_name
        return '/media/%s/%s.%s' % (self.path, filename, self.extension)
