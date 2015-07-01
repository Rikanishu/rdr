# encoding: utf-8

from datetime import datetime, timedelta

from flask import render_template
from rdr.components.blueprints import RichBlueprint
from rdr.application import app
from rdr.components.csrf import get_csrf_token
from rdr.modules.users.models import User
from rdr.modules.users.session import login_required, user_session
from rdr.components.helpers import json


blueprint = RichBlueprint('home', __name__, template_folder='templates')

@blueprint.route('/')
def index():

    from rdr.modules.home.static import builder
    from rdr.application.i18n import get_labels_catalog, get_locale
    import json

    builder.collect_links()
    lang = get_locale().language
    init_data = {}
    if user_session.is_auth:
        init_data['user'] = user_session.identity.to_dict()
    init_data['csrfToken'] = get_csrf_token()
    init_data['l10nData'] = get_labels_catalog()
    init_data['appOptions'] = {
        'isSignupEnabled': app.config['SIGNUP_ENABLED']
    }
    init_data['availableLanguages'] = app.config['LANGUAGES']
    init_data['language'] = lang

    return render_template('index.jhtml',
                           statics=builder,
                           init_data=json.dumps(init_data),
                           lang=lang)


@blueprint.route('/home/dashboard')
@json.wrap
@login_required
def home_dashboard():
    from rdr.modules.home.dashboard.last_visit_news import LastVisitNewsGenerator, PopularNewsGenerator
    from rdr.modules.feeds.articles.status import UserArticleRecord

    articles = []
    news_type = 'lastvisit'
    identity = User.query.filter(User.id == user_session.identity.id).one()
    if not identity.last_visit or (datetime.now() - identity.last_visit) >= timedelta(minutes=20):
        gen = LastVisitNewsGenerator(user_session.identity)
        articles = gen.fetch_articles()
    if not articles:
        news_type = 'popular'
        gen = PopularNewsGenerator(user_session.identity, use_cache=False)
        articles = gen.fetch_articles()
    articles = UserArticleRecord.wrap_articles_list(articles)
    return {
        'success': True,
        'news': [x.to_dict() for x in articles],
        'type': news_type
    }


@blueprint.route('/home/check-show-tutorial')
@json.wrap
@login_required
def check_tutorial_show():
    identity = User.query.filter(User.id == user_session.identity.id).one()
    show_tutorial = (identity.profile and identity.profile.show_tutorial)
    return {
        'success': True,
        'showTutorial': show_tutorial
    }


app.register_blueprint(blueprint)
