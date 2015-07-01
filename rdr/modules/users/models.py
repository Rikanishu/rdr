# encoding: utf-8

from rdr.application.database import db, ReprMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import validates
import marshal

ROLE_USER = 1
ROLE_ADMIN = 2


class User(db.Model, ReprMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), index=True, default='')
    email = db.Column(db.String(255), index=True, unique=True)
    password = db.Column(db.String(255), index=True)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    active = db.Column(db.Boolean, default=True)
    last_visit = db.Column(db.DateTime, index=True)

    profile = db.relationship("Profile", lazy='joined', uselist=False)

    @property
    def is_admin(self):
        return self.role == ROLE_ADMIN

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @validates('password')
    def update_password(self, key, password):
        return User.gen_password(password)

    def repr(self):
        return '<User [%s] "%s">', self.id, self.username

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.username,
            'email': self.email,
            'isAdmin': self.role == ROLE_ADMIN
        }
        if self.profile and self.profile.image:
            data['imageSrc'] = self.profile.image.src('middle')
        else:
            data['imageSrc'] = 'static/img/users/default.png'
        data['showTutorial'] = (self.profile and self.profile.show_tutorial)
        return data

    @classmethod
    def gen_password(cls, password):
        return generate_password_hash(password)


class Profile(db.Model, ReprMixin):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'))
    show_tutorial = db.Column(db.Boolean)
    lang = db.Column(db.String(12))
    dropbox_access_token = db.Column(db.String(512))

    user = db.relationship("User", uselist=False)
    image = db.relationship("Image", uselist=False)

    def repr(self):
        return '<Profile [%s] "%s">', self.id, self.user_id


class Action(db.Model, ReprMixin):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    date = db.Column(db.DateTime, index=True)
    type = db.Column(db.String(64))
    binary_data = db.Column(db.LargeBinary(8192))

    @property
    def data(self):
        if self.data:
            return marshal.loads(self.binary_data)
        return None

    @data.setter
    def data(self, data):
        self.binary_data = marshal.dumps(data)

    def repr(self):
        return '<Action [%s] "%s">', self.id, self.user_id

