# encoding: utf-8

from datetime import datetime
from flask import request, abort

from rdr.application.database import db
from rdr.modules.feeds.blueprint import blueprint
from rdr.components.helpers import json
from rdr.modules.users.session import login_required, session_user
from rdr.modules.feeds.models import OfflineReadQueue, OfflineReadQueueTask

@blueprint.route('/offline-read-queue/add-article', methods=['POST'])
@json.wrap
@login_required
def add_article():
    body = json.get_request_body()
    article_id = body['articleId']
    queue = OfflineReadQueue.query.filter((OfflineReadQueue.user_id == session_user.identity.id) &
                                          (OfflineReadQueue.article_id == article_id)).first()
    if not queue:
        queue = OfflineReadQueue(user_id=session_user.identity.id, article_id=article_id, add_date=datetime.now())
        db.session.add(queue)
        db.session.commit()
    return {
        'success': True
    }


@blueprint.route('/offline-read-queue/remove-article', methods=['POST'])
@json.wrap
@login_required
def remove_article():
    body = json.get_request_body()
    article_id = body['articleId']
    queue = OfflineReadQueue.query.filter((OfflineReadQueue.user_id == session_user.identity.id) &
                                          (OfflineReadQueue.article_id == article_id)).first()
    if not queue:
        raise json.NotFound('Queue not found')
    db.session.delete(queue)
    db.session.commit()
    return {
        'success': True
    }


@blueprint.route('/offline-read-queue/add-feed-unread', methods=['POST'])
@json.wrap
@login_required
def add_feed_unread():
    from rdr.modules.feeds.articles.unread import FeedUnreadArticlesSet
    from rdr.modules.feeds.models import Feed

    body = json.get_request_body()
    feed_id = body['feedId']
    feed = Feed.query.filter(Feed.id == feed_id).first()
    if not feed:
        raise json.NotFound('Feed not found')
    unread_set = FeedUnreadArticlesSet(session_user.user, feed)
    for article in unread_set.articles:
        queue = OfflineReadQueue.query.filter((OfflineReadQueue.user_id == session_user.identity.id) &
                                              (OfflineReadQueue.article_id == article.id)).first()
        if not queue:
            queue = OfflineReadQueue(user_id=session_user.identity.id, article_id=article.id, add_date=datetime.now())
            db.session.add(queue)
    db.session.commit()
    return {
        'success': True
    }

@blueprint.route('/offline-read-queue/clear-queue', methods=['POST'])
@login_required
@json.wrap
def clear_queue():
    queues = OfflineReadQueue.query.filter(OfflineReadQueue.user_id == session_user.identity.id)
    for queue in queues:
        db.session.delete(queue)
    db.session.commit()
    return {
        'success': True
    }


@blueprint.route('/offline-read-queue/list')
@json.wrap
@login_required
def queue_list():
    page = 1
    if 'page' in request.args:
        page = int(request.args['page'])
    user = session_user.user

    from rdr.modules.feeds.models import Article
    from rdr.modules.feeds.articles.status import UserArticleRecord

    articles_pagination = Article.query \
        .join(OfflineReadQueue, (OfflineReadQueue.user_id == user.id) & (OfflineReadQueue.article_id == Article.id)) \
        .options(db.joinedload(Article.statuses),
                 db.joinedload(Article.feed)) \
        .filter((Article.active == True)).order_by(OfflineReadQueue.add_date.asc()) \
        .paginate(page, per_page=60, error_out=False)

    records = UserArticleRecord.wrap_articles_list(articles_pagination.items)

    return {
        'success': True,
        'articles': [x.to_dict(full_text=True) for x in records]
    }


@blueprint.route('/offline-read-queue/generate-file', methods=['POST'])
@login_required
@json.wrap
def generate_file():
    from rdr.tasks.jobs.offline_reading import generate_file
    from rdr.application.i18n import get_locale
    from flask import request

    file_format = 'PDF'
    task = OfflineReadQueueTask(user_id=session_user.identity.id,
                                status=OfflineReadQueueTask.STATUS_STARTED,
                                file_format=file_format)
    db.session.add(task)
    db.session.commit()
    generate_file.apply_async(args=(task.id,), kwargs={
        'app_url': request.url_root.rstrip('/'),
        'file_format': file_format,
        'lang': get_locale().language
    }, retry=False)

    return {
        'success': True,
        'taskId': task.id
    }

@blueprint.route('/offline-read-queue/check-task-completed/<int:task_id>')
@login_required
@json.wrap
def check_task_status(task_id):
    task = OfflineReadQueueTask.query.filter(OfflineReadQueueTask.id == task_id).first()
    if not task:
        raise json.NotFound()
    return {
        'success': True,
        'isCompleted': task.status != OfflineReadQueueTask.STATUS_STARTED
    }


@blueprint.route('/offline-read-queue/download-file/<int:task_id>')
@login_required
def download_file(task_id):
    import os
    from flask import make_response

    task = OfflineReadQueueTask.query.filter(OfflineReadQueueTask.id == task_id).first()
    if not task:
        raise abort(404, description='Task status not found')
    if task.status != OfflineReadQueueTask.STATUS_FILE_GENERATED:
        raise abort(500, description='File is not generated')
    tmpfile = task.out_file
    if not os.path.exists(tmpfile):
        abort(404, description='Unknown file')
    with open(tmpfile) as f:
        res = make_response(f.read())
    os.unlink(tmpfile)
    res.headers["Content-Disposition"] = 'attachment; ' \
                                         'filename=Articles-%s.pdf' % (datetime.now().strftime('%Y-%m-%d %H:%M'))
    res.headers["Content-Type"] = "application/pdf"
    task.status = OfflineReadQueueTask.STATUS_DONE
    db.session.commit()

    return res


@blueprint.route('/offline-read-queue/save-to-dropbox/<int:task_id>')
@login_required
@json.wrap
def save_to_dropbox(task_id):
    pass