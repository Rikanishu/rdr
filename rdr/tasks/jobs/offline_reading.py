# encoding: utf-8

from rdr.tasks import celery


@celery.task()
def generate_file(task_id, app_url='http://localhost:9000', file_format='PDF', lang='en'):

    from rdr.modules.users.session import session_user
    from rdr.modules.feeds.models import OfflineReadQueueTask
    task = OfflineReadQueueTask.query.filter(OfflineReadQueueTask.id == task_id).one()
    user = task.user
    session_user.auth(user)

    from rdr.application.i18n import format_datetime, gettext, ngettext, set_global_lang
    set_global_lang(lang)

    from rdr.application.database import db
    from rdr.modules.feeds.models import Article, OfflineReadQueue
    from rdr.modules.feeds.articles.status import UserArticleRecord

    articles = Article.query \
        .join(OfflineReadQueue, (OfflineReadQueue.user_id == user.id) & (OfflineReadQueue.article_id == Article.id)) \
        .options(db.joinedload(Article.statuses),
                 db.joinedload(Article.feed)) \
        .filter((Article.active == True)).order_by(OfflineReadQueue.add_date.asc())

    records = UserArticleRecord.wrap_articles_list(articles)
    dicts = [x.to_dict(full_text=True) for x in records]

    if not dicts:
        task.status = OfflineReadQueueTask.STATUS_REJECTED
        db.session.commit()
        return False

    from jinja2 import Environment, FileSystemLoader
    import os
    from datetime import datetime

    env = Environment(extensions=['jinja2.ext.i18n', 'jinja2.ext.autoescape', 'jinja2.ext.with_'], autoescape=True, loader=FileSystemLoader(
        os.path.join(os.path.dirname(os.path.realpath(__file__)),
                     '..',
                     '..',
                     'modules',
                     'feeds',
                     'templates',
                     'offline-reading')
        )
    )
    env.install_gettext_callables(gettext, ngettext, True)
    template = env.get_template('pdf-std.jhtml')
    content = template.render(articles=dicts,
                              url=app_url,
                              username=user.username,
                              gen_date=format_datetime(datetime.now(), 'dd MMM yyyy HH:mm'))

    import pdfkit
    from tempfile import NamedTemporaryFile

    pdf_opts = {
        'page-size': 'Letter'
    }
    f = NamedTemporaryFile(delete=False)
    pdfkit.from_string(content, f.name, options=pdf_opts)
    task.status = OfflineReadQueueTask.STATUS_FILE_GENERATED
    task.out_file = f.name
    db.session.commit()
    return True