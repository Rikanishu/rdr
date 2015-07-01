# encoding: utf-8

from flask.ext.restful import Api, Resource, abort, reqparse
from rdr.application import app
from flask import session


api = Api(app, prefix="/api")


def token_required(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper
