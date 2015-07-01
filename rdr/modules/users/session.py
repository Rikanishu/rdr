# encoding: utf-8

import functools
from flask import session, g, has_request_context
from werkzeug.exceptions import Forbidden
from rdr.modules.users.models import User
from rdr.application import app

@app.before_request
def _init_request_session():
    g.session_identity = None
    if 'user' in session:
        user = User.query.get(session['user'])
        # db.session.expunge(user)
        if not user:
            raise UserSessionException('Can\'t recognize user model')
        g.session_identity = user


class UserSessionException(Exception):
    pass


class NotAuthException(UserSessionException):
    pass


class UserSession(object):

    @property
    def user(self):
        return self.identity

    @user.setter
    def user(self, user):
        self.identity = user

    @property
    def identity(self):
        if not self.is_auth:
            raise NotAuthException('User is not authorised, check is_auth first')
        return g.session_identity

    @identity.setter
    def identity(self, user):
        # db.session.expunge(user)
        g.session_identity = user
        if has_request_context():
            session['user'] = user.id

    @property
    def dict(self):
        return session

    @property
    def is_auth(self):
        return 'session_identity' in g and g.session_identity is not None

    def auth(self, user):
        self.user = user

    def quit(self):
        g.session_identity = None
        if has_request_context():
            session.pop('user', None)


user_session = UserSession()
session_user = user_session


def login_required(f):
    """
    Check if user logged or show forbidden page
    This function don't check user permissions

    :param f: decorated function
    """
    @functools.wraps(f)
    def wrap(*args, **kwargs):
        if not user_session.is_auth:
            raise Forbidden()
        return f(*args, **kwargs)
    return wrap