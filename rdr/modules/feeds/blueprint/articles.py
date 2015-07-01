# encoding: utf-8

from datetime import datetime, timedelta

from flask import request

from rdr.modules.feeds.articles.status import UserArticleRecord, UserPackageRecord
from rdr.modules.feeds.blueprint import blueprint
from rdr.components.helpers import json, html
from rdr.modules.users.session import login_required, session_user
from rdr.application.database import db
from rdr.modules.feeds.models import Article, ArticleStatus, ArticleFavorite, Feed
from rdr.modules.feeds.articles.sync import ArticlesSynchronizer



@blueprint.route('/<int:feed_id>/articles/list')
@json.wrap
@login_required
def articles_list(feed_id):
    page = 1
    if 'page' in request.args:
        page = int(request.args['page'])

    feed = Feed.query.filter(Feed.id == feed_id).first()
    if not feed:
        raise json.InvalidRequest("Unknown feed id")
    if not feed.active:
        activate_feed(feed)
    articles_pagination = Article.query \
        .filter((Article.feed_id == feed_id) & (Article.active == True)) \
        .order_by(Article.published.desc()) \
        .options(db.joinedload(Article.feed)) \
        .paginate(page, per_page=40, error_out=False)

    records = UserArticleRecord.wrap_articles_list(articles_pagination.items)
    feed_record = UserPackageRecord.wrap_package(feed)

    return {
        'success': True,
        'articles': [x.to_dict() for x in records],
        'feed': feed_record.to_dict()
    }


@blueprint.route('/<int:feed_id>/articles/sync')
@json.wrap
@login_required
def articles_sync(feed_id):
    page = 1
    feed = Feed.query.filter(Feed.id == feed_id).first()
    if not feed:
        raise json.InvalidRequest("Unknown feed id")
    default_update_pause_seconds = 300
    if not feed.last_update or (datetime.now() - feed.last_update) > timedelta(seconds=default_update_pause_seconds):
        synchronizer = ArticlesSynchronizer(feed)
        synchronizer.sync()
    articles_pagination = Article.query \
        .filter((Article.feed_id == feed_id) & (Article.active == True)) \
        .order_by(Article.published.desc()) \
        .options(db.joinedload(Article.feed)) \
        .paginate(page, per_page=40, error_out=False)

    records = UserArticleRecord.wrap_articles_list(articles_pagination.items)
    feed_record = UserPackageRecord.wrap_package(feed)

    return {
        'success': True,
        'articles': [x.to_dict() for x in records],
        'feed': feed_record.to_dict()
    }


@blueprint.route('/unread/articles/list')
@json.wrap
@login_required
def articles_unread_list():
    page = 1
    if 'page' in request.args:
        page = int(request.args['page'])

    from rdr.modules.feeds.articles.unread import TotalUnreadArticlesSet

    unread_set = TotalUnreadArticlesSet(session_user.user)
    articles_pagination = unread_set.query.options(db.joinedload(Article.feed)) \
        .paginate(page, per_page=60, error_out=False)
    records = UserArticleRecord.wrap_articles_list(articles_pagination.items)

    return {
        'success': True,
        'articles': [x.to_dict() for x in records]
    }


@blueprint.route('/favorites/articles/list')
@json.wrap
@login_required
def article_favorites_list():
    page = 1
    if 'page' in request.args:
        page = int(request.args['page'])
    user = session_user.user

    from rdr.modules.feeds.models import ArticleFavorite

    articles_pagination = Article.query \
        .join(ArticleFavorite, (ArticleFavorite.user_id == user.id) & (ArticleFavorite.article_id == Article.id)) \
        .options(db.joinedload(Article.statuses),
                 db.joinedload(Article.feed)) \
        .filter((Article.active == True)).order_by(ArticleFavorite.fav_date.desc()) \
        .paginate(page, per_page=60, error_out=False)

    records = UserArticleRecord.wrap_articles_list(articles_pagination.items)

    return {
        'success': True,
        'articles': [x.to_dict() for x in records]
    }


@blueprint.route('/favorites/articles/add', methods=['POST'])
@json.wrap
@login_required
def article_add_to_favorites():
    body = json.get_request_body()
    article_id = body['articleId']
    fav = ArticleFavorite.query \
        .filter((ArticleFavorite.user_id == session_user.user.id) & (ArticleFavorite.article_id == article_id)) \
        .first()
    if not fav:
        fav = ArticleFavorite(article_id=article_id, user_id=session_user.user.id, fav_date=datetime.now())
        db.session.add(fav)
        db.session.commit()

    return {
        'success': True
    }


@blueprint.route('/favorites/articles/remove', methods=['POST'])
@json.wrap
@login_required
def article_remove_from_favorites():
    body = json.get_request_body()
    article_id = body['articleId']
    fav = ArticleFavorite.query \
        .filter((ArticleFavorite.user_id == session_user.user.id) & (ArticleFavorite.article_id == article_id)) \
        .first()
    if fav:
        db.session.delete(fav)
        db.session.commit()

    return {
        'success': True
    }


@blueprint.route('/articles/<int:article_id>/full-text')
@json.wrap
@login_required
def article_full_text(article_id):
    article = Article.query.filter(Article.id == article_id).one()
    full_text = fetch_full_text(article)

    return {
        'success': True,
        'fullText': full_text.to_dict()
    }


@blueprint.route('/articles/mark-as-read', methods=['POST'])
@json.wrap
@login_required
def article_mark_as_read():
    body = json.get_request_body()
    article_id = body['articleId']
    existed_status = ArticleStatus.query \
        .filter((ArticleStatus.article_id == article_id) & (ArticleStatus.user_id == session_user.user.id)) \
        .first()
    if existed_status:
        existed_status.status = ArticleStatus.STATUS_READ
    else:
        article_status = ArticleStatus()
        article_status.user_id = session_user.user.id
        article_status.article_id = article_id
        article_status.status = ArticleStatus.STATUS_READ
        article_status.read_date = datetime.now()
        db.session.add(article_status)
    db.session.commit()

    return {
        'success': True
    }


@blueprint.route('/articles/<int:article_id>/info')
@json.wrap
@login_required
def get_article_info(article_id):
    full_text = request.args.get('full-text')
    article = Article.query.filter(Article.id == article_id).first()
    if not article:
        raise json.NotFound()
    rec = UserArticleRecord.wrap_article(article)
    res = {'success': True, 'article': rec.to_dict()}
    if full_text:
        model = fetch_full_text(article)
        if model:
            res['fullText'] = model.to_dict()
    return res


# todo: get method instead
@blueprint.route('/articles/search', methods=['POST'])
@json.wrap
@login_required
def search():
    page = 1
    body = json.get_request_body()
    if 'page' in body:
        page = int(body['page'])
    params = {}
    if 'type' in body:
        params['filter_criteria'] = body['type']
    if 'where' in body:
        params['where'] = body['where']
    from rdr.modules.feeds.search import ArticleSearchProvider
    if 'feed' in body:
        provider = ArticleSearchProvider(feeds=[int(body['feed'])], user=session_user.identity)
    else:
        provider = ArticleSearchProvider(user=session_user.identity)
    ids = provider.search(body['query'], **params)
    if ids:
        articles_pagination = Article.query \
            .options(db.joinedload(Article.statuses),
                     db.joinedload(Article.feed)) \
            .filter((Article.active == True) & (Article.id.in_(ids))).order_by(Article.published.desc()) \
            .paginate(page, per_page=60, error_out=False)

        records = UserArticleRecord.wrap_articles_list(articles_pagination.items)
        records = [x.to_dict() for x in records]
    else:
        records = []
    return {
        'success': True,
        'articles': records
    }


def activate_feed(feed):
    synchronizer = ArticlesSynchronizer(feed)
    return synchronizer.sync()

def fetch_full_text(article):
    from rdr.modules.feeds.models import ArticleFullText
    full_text = ArticleFullText.query.filter(ArticleFullText.article_id == article.id).first()
    if not full_text:
        from rdr.modules.feeds.full_text import FullTextProvider
        from rdr.modules.feeds.search import ArticleSearchIndex


        provider = FullTextProvider.provider()
        full_text_result = provider.fetch_article_full_text(article)
        if full_text_result:
            full_text = ArticleFullText(article_id=article.id,
                                        text=html.nl2p(full_text_result.safe_text),
                                        image_src=full_text_result.primary_image)
            if not article.preview_image_src:
                article.preview_image_src = full_text_result.primary_image
        else:
            full_text = ArticleFullText(article_id=article.id,
                                        text=html.nl2p(article.preview_text),
                                        image_src=article.preview_image_src)
        db.session.add(full_text)
        db.session.commit()

        search_provider = ArticleSearchIndex(article)
        search_provider.create_full_text_index(full_text)
    return full_text