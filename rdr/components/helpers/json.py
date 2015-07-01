# encoding: utf-8

import functools

from flask import jsonify, request
from werkzeug.exceptions import HTTPException
from werkzeug.wrappers import BaseResponse
from rdr.application import app


def trace_exception():
    import traceback
    tr = traceback.format_exc()
    res = []
    for l in tr.split('\n'):
        res.append(l)
    return res


def result(*args, **kwargs):
    return jsonify(*args, **kwargs)


def error(code=500, success=False, **kwargs):
    res = jsonify(success=success, **kwargs)
    res.status_code = code
    return res


def wrap(f):
    @functools.wraps(f)
    def run_func(*args, **kwargs):
        try:
            res = f(*args, **kwargs)
            if not isinstance(res, BaseResponse):
                res = result(**res)
            return res
        except HTTPException as e:
            exres = {'message': e.description}
            if app.debug:
                exres['trace'] = trace_exception()
            app.logger.exception(e)
            return error(e.code, **exres)
        except Exception as e:
            exres = {'message': 'Error while processing request'}
            if app.debug:
                exres['message'] = e.message
                exres['trace'] = trace_exception()
            app.logger.exception(e)
            return error(500, **exres)
    return run_func


def get_request_body():
    json = request.get_json()
    if json is None:
        json = {}
    elif type(json) != dict:
        json = {
            request: json
        }
    return RequestBody(json)


class RequestBody(dict):

    def __missing__(self, key):
        raise InvalidRequest('"%s"" is required request param' % key)


class InvalidRequest(HTTPException):

    description = 'Invalid request'
    code = 400


class ProcessError(HTTPException):

    description = 'Error while processing request'
    code = 500

class NotFound(HTTPException):

    description = 'Not found'
    code = 404
