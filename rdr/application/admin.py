# encoding: utf-8

from flask.ext.admin import Admin, AdminIndexView
from rdr.application import app
from flask.ext.admin.contrib.sqla import ModelView


def admin_access():
    from rdr.modules.users.session import session_user
    return session_user.is_auth and session_user.user.is_admin


class IndexView(AdminIndexView):

    def is_accessible(self):
        return admin_access()


class DatabaseModelView(ModelView):

    def is_accessible(self):
        return admin_access()


admin = Admin(app, name='Reader', index_view=IndexView())