# encoding: utf-8

from datetime import datetime

from rdr.modules.feeds.blueprint import blueprint
from rdr.components.helpers import json
from rdr.modules.users.session import login_required, session_user
from rdr.modules.feeds.models import Feed, ArticleStatus
from werkzeug.exceptions import NotFound
from rdr.application.database import db


@blueprint.route('/mark-all-as-read', methods=['POST'])
@json.wrap
@login_required
def feed_mark_all_as_read():
    from rdr.modules.feeds.articles.unread import FeedUnreadArticlesSet

    body = json.get_request_body()
    feed_id = body['feedId']
    feed = Feed.query.filter(Feed.id == feed_id).first()
    if not feed:
        raise NotFound("Feed not found")
    unread_set = FeedUnreadArticlesSet(session_user.user, feed)
    for article in unread_set.articles:
        article_status = ArticleStatus()
        article_status.user_id = session_user.user.id
        article_status.article_id = article.id
        article_status.status = ArticleStatus.STATUS_READ
        article_status.read_date = datetime.now()
        db.session.add(article_status)
    db.session.commit()
    return {
        'success': True
    }


@blueprint.route('/mark-all-unread-as-read', methods=['POST'])
@json.wrap
@login_required
def feed_mark_unread_as_read():
    from rdr.modules.feeds.articles.unread import TotalUnreadArticlesSet
    unread_set = TotalUnreadArticlesSet(session_user.user)
    for article in unread_set.articles:
        article_status = ArticleStatus()
        article_status.user_id = session_user.user.id
        article_status.article_id = article.id
        article_status.status = ArticleStatus.STATUS_READ
        article_status.read_date = datetime.now()
        db.session.add(article_status)
    db.session.commit()
    return {
        'success': True
    }


@blueprint.route('/<int:feed_id>/info')
@json.wrap
@login_required
def get_feed_info(feed_id):
    from rdr.modules.feeds.articles.status import UserPackageRecord

    feed = Feed.query.filter(Feed.id == feed_id).first()
    if not feed:
        raise NotFound("Feed not found")
    rec = UserPackageRecord.wrap_package(feed)
    return {
        'success': True,
        'feed': rec.to_dict()
    }
