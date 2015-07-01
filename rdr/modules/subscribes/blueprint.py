# encoding: utf-8

from rdr.application.database import db
from rdr.components.blueprints import RichBlueprint
from flask import jsonify, request, abort
from rdr.application import app
from rdr.modules.users.session import login_required, session_user
from rdr.modules.subscribes.models import Subscribe
from rdr.components.helpers import json

blueprint = RichBlueprint('subscribes', __name__,
                          url_prefix="/subscribes", template_folder='templates')


def make_subscribes_hierarchy(subscribes):
    folders = {}
    items = []
    for sub in subscribes:
        if sub.type == Subscribe.TYPE_FOLDER:
            folders[sub.id] = {
                'subscribe': sub,
                'feeds': []
            }
        elif sub.type == Subscribe.TYPE_FEED:
            if sub.feed:
                items.append(sub)
    for sub in items:
        if sub.parent_id == 0:
            folders[sub.id] = {
                'subscribe': sub,
                'feeds': []
            }
        if sub.parent_id in folders:
            folders[sub.parent_id]['feeds'].append(sub)
    hierarchy = []
    for folder in folders.values():
        folder['feeds'].sort(key=lambda f: f.order)
        hierarchy.append(folder)
    hierarchy.sort(key=lambda f: f['subscribe'].order)
    result = []
    for folder in hierarchy:
        folder['feeds'] = map(prepare_subscribe, folder['feeds'])
        folder['subscribe'] = prepare_subscribe(folder['subscribe'])
        folder['subscribe']['feeds'] = folder['feeds']
        result.append(folder['subscribe'])
    return result


def prepare_subscribe(subscribe):
    result = subscribe.to_dict()
    if subscribe.type == Subscribe.TYPE_FEED:
        from rdr.modules.feeds.articles.unread import FeedUnreadArticlesSet
        unread_set = FeedUnreadArticlesSet(session_user.user, subscribe.feed)
        result['unreadCount'] = unread_set.count
    return result


def find_package(ptype, pid):
    if ptype == Subscribe.TYPE_FEED:
        from rdr.modules.feeds.models import Feed
        return Feed.query.filter(Feed.id == pid).one()
    raise Exception('Unknown package id')


@blueprint.route('/list')
@json.wrap
@login_required
def subscribes_list():
    user_subscribes = Subscribe.query.filter((Subscribe.user_id == session_user.user.id) &
                                       (Subscribe.active == True))
    hierarchy = make_subscribes_hierarchy(user_subscribes)

    from rdr.modules.feeds.articles.unread import TotalUnreadArticlesSet
    total_unread_set = TotalUnreadArticlesSet(session_user.user)

    return {
        'success': True,
        'subscribes': hierarchy,
        'totalUnreadCount': total_unread_set.count
    }


@blueprint.route('/create-folder', methods=['POST'])
@json.wrap
@login_required
def create_folder():
    body = json.get_request_body()
    folder_name = body['name']
    if not folder_name:
        raise json.InvalidRequest('Folder name must be non-empty string')
    sub = Subscribe(user_id=session_user.user.id, parent_id=0,
                    name=folder_name, type=Subscribe.TYPE_FOLDER,
                    order=10, active=True)
    db.session.add(sub)
    db.session.commit()
    return {
        'success': True,
        'subscribe': sub.to_dict()
    }

@blueprint.route('/new-subscribe', methods=['POST'])
@json.wrap
@login_required
def new_subscribe():
    body = json.get_request_body()
    package_id = body['packageId']
    package_type = body['packageType']
    folder = body['folder']
    if not (package_id and package_type and folder >= 0):
        raise json.InvalidRequest()
    current_user_id = session_user.user.id
    if folder != 0:
        folder_subscribe = Subscribe.query.filter((Subscribe.user_id == current_user_id) &
                                                  (Subscribe.id == folder)).first()
        if not folder_subscribe:
            raise Exception("Subscriber folder is not exists")
    package = find_package(package_type, package_id)
    if not package:
        raise Exception("Package is not exists")
    sub = Subscribe(user_id=session_user.user.id, parent_id=folder, type=Subscribe.TYPE_FEED,
                    name=package.title, order=20, active=True, feed_id=package.id)
    db.session.add(sub)
    db.session.commit()

    from rdr.modules.feeds.articles.unread import TotalUnreadArticlesSet
    total_unread_set = TotalUnreadArticlesSet(session_user.user)
    sub_dict = prepare_subscribe(sub)

    return {
        'success': True,
        'subscribe': sub_dict,
        'totalUnreadCount': total_unread_set.count
    }


@blueprint.route('/stats')
@json.wrap
@login_required
def stats():
    from rdr.modules.feeds.stats import StatsGenerator
    stats_type = request.args.get('type', StatsGenerator.DATES_LAST_WEEK)

    stats_gen = StatsGenerator(dates=stats_type)
    stats = stats_gen.generate_stats()

    return {
        'success': True,
        'stats': stats
    }


@blueprint.route('/save', methods=['POST'])
@json.wrap
@login_required
def save():
    body = json.get_request_body()
    root_subscribes = body['rootSubscribes']
    folders = body['folders']

    subscriptions = Subscribe.query.filter(Subscribe.user_id == session_user.identity.id)
    for sub in subscriptions:
        db.session.delete(sub)

    for folder_data in folders:
        folder_name = folder_data['name']
        folder = Subscribe(user_id=session_user.identity.id, parent_id=0,
                        name=folder_name, type=Subscribe.TYPE_FOLDER,
                        order=10, active=True, feed_id=None)
        db.session.add(folder)
        db.session.flush()
        folder_feeds = folder_data['feeds']
        if folder_feeds:
            for sub_data in folder_feeds:
                feed_id = sub_data['feedId']
                feed_name = sub_data['name']
                sub = Subscribe(user_id=session_user.identity.id, parent_id=folder.id,
                                name=feed_name, type=Subscribe.TYPE_FEED,
                                order=20, active=True, feed_id=feed_id)
                db.session.add(sub)

    for sub_data in root_subscribes:
        feed_id = sub_data['feedId']
        feed_name = sub_data['name']
        sub = Subscribe(user_id=session_user.identity.id, parent_id=0,
                        name=feed_name, type=Subscribe.TYPE_FEED,
                        order=20, active=True, feed_id=feed_id)
        db.session.add(sub)

    db.session.commit()

    return {
        'success': True
    }


@blueprint.route('/import', methods=['POST'])
@json.wrap
@login_required
def import_():
    if 'file' not in request.files:
        raise json.InvalidRequest()
    f = request.files['file']
    from rdr.modules.subscribes.opml import OPMLImporter
    importer = OPMLImporter(f.stream.read())
    importer.run()
    return {
        'success': True
    }


@blueprint.route('/export')
@json.wrap
@login_required
def export():
    from rdr.modules.subscribes.opml import OPMLExporter
    from flask import Response
    exporter = OPMLExporter()
    opml = exporter.make_opml()

    return Response(opml, mimetype='text/x-opml+xml', headers={
        "Content-Disposition": "attachment;filename=reader.opml"
    })

app.register_blueprint(blueprint)