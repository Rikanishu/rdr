# encoding: utf-8

import os, time
from rdr.application import app

tz = app.config.get('TIMEZONE')
os.environ['TZ'] = tz
time.tzset()


def convert_to_local(date):
    if date.tzinfo:
        from pytz import utc
        from dateutil.tz import tzlocal
        date = date.astimezone(utc).replace(tzinfo=None)
        date = date + tzlocal().utcoffset(date)
    return date
