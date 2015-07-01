# encoding: utf-8

from celery import Celery
from rdr.application import app
from .schedule.feeds import schedule as feeds_schedule

schedule = {}
schedule.update(feeds_schedule)
conf = app.config.copy()
conf['CELERYBEAT_SCHEDULE'] = schedule

celery = Celery(app.import_name, broker=conf['CELERY_BROKER_URL'])
celery.conf.update(conf)

TaskBase = celery.Task


class ContextTask(TaskBase):

    abstract = True

    def __call__(self, *args, **kwargs):
        with app.app_context():
            return TaskBase.__call__(self, *args, **kwargs)


celery.Task = ContextTask

from .jobs import feeds
from .jobs import offline_reading
