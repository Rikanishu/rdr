# encoding: utf-8

from rdr.application import app
from flask import request, session, abort
from uuid import uuid4
from hashlib import sha1

@app.before_request
def csrf_protect():
    if app.config.get('CSRF_ENABLED', False) and request.method == "POST":
        token = session.get('_csrf_token', None)
        if not token or token != request.headers.get('X-CSRFToken'):
            abort(400)


def get_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = sha1(uuid4().hex).hexdigest()
    return session['_csrf_token']