# encoding: utf-8

from flask import request
from rdr.application import app
from flask.ext.babel import (Babel,
                             gettext,
                             ngettext,
                             lazy_gettext,
                             format_datetime,
                             format_date,
                             get_locale,
                             get_translations)

babel = Babel(app)
_lang = None

@babel.localeselector
def locale_selector():
    if _lang:
        return _lang

    from rdr.modules.users.session import session_user

    if session_user.is_auth:
        profile = session_user.identity.profile
        if profile and profile.lang:
            return profile.lang
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys())


def get_full_catalog():
    t = get_translations()
    if t and t._catalog:
        return t._catalog
    return {}


def get_labels_catalog():
    cat = get_full_catalog()
    items = {}
    for (label, translate) in cat.iteritems():
        if label and isinstance(label, basestring):
            items[label] = translate
    return items


def set_global_lang(lang):
    global _lang
    _lang = lang