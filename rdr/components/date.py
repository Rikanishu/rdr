# encoding: utf-8

from datetime import datetime

from rdr.application.i18n import gettext, ngettext, format_datetime


def relative_date_format(dt):
    diff = datetime.now() - dt
    s = diff.seconds
    if diff.days > 30 or diff.days < 0:
        return format_datetime(dt, 'dd MMM yyyy HH:mm')
    elif diff.days == 1:
        return ngettext('%(days)d day ago', '%(days)d days ago', 1, days=1)
    elif diff.days > 1:
        return ngettext('%(days)d day ago', '%(days)d days ago', diff.days, days=diff.days)
    elif s <= 1:
        return gettext('just now')
    elif s < 60:
        return ngettext('%(seconds)d second ago', '%(seconds)d seconds ago', s, seconds=s)
    elif s < 120:
        return ngettext('%(minutes)d minute ago', '%(minutes)d minutes ago', 1, minutes=1)
    elif s < 3600:
        return ngettext('%(minutes)d minute ago', '%(minutes)d minutes ago', s / 60, minutes=(s / 60))
    elif s < 7200:
        return ngettext('%(hours)d hour ago', '%(hours)d hours ago', 1, hours=1)
    else:
        return ngettext('%(hours)d hour ago', '%(hours)d hours ago', s / 3600, hours=(s / 3600))