# encoding: utf-8

from rdr.application.admin import admin, DatabaseModelView
from rdr.application.database import db

from rdr.modules.feeds.models import Feed, Article, ArticleFullText

admin.add_view(DatabaseModelView(Feed, db.session))
admin.add_view(DatabaseModelView(Article, db.session))
admin.add_view(DatabaseModelView(ArticleFullText, db.session))