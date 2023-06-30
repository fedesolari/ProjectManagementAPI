import os
import datetime
import functools
import io
from threading import Thread
from flask import current_app, jsonify, request
import requests
from log import LOG
from werkzeug.exceptions import Unauthorized, Forbidden
from project.responses.response_constants import response_code_map
from marshmallow import Schema, fields
from sqlalchemy import func
import jwt
from werkzeug.exceptions import Forbidden, NotFound

DATE_FORMAT = '%d/%m/%Y'
DATA_WHEN_NONE = '-'
DATE_FORMAT_WITHOUT_DAY = '%m/%Y'


def auth_required(allowed_profiles=[]):
    """
    This decorator will check an auth_token received on the API
    layer and inject the related user into the called method
    """

    def method_wrap(method):
        @functools.wraps(method)
        def wrapper(*args, **kwds):

            token = request.args.get('token')

            if not token:
                raise Unauthorized(description="Debe iniciar sesión para realizar esta acción.")

            # pass payload to wrapper method as last parameter
            kwds['jwt_payload'] = {"token": token}

            return method(*args, **kwds)

        return wrapper
    return method_wrap


def get_general_response_schema(result_type):
    return Schema.from_dict({
        "code": fields.Integer(),
        "message": fields.Str(),
        "result": fields.List(fields.Nested(result_type))
    })


def generate_response(code, result_list, status):
    response = jsonify({'code': code, 'message': response_code_map.get(code), "result": result_list})
    response.status = status
    return response


def log_method(method):
    """
    This decorator measure the time taken by the method and log it with its information.
    """

    @functools.wraps(method)
    def wrapper(*args, **kwds):
        LOG.info(f'Running method {method.__name__} with params {args}')
        begin = datetime.datetime.now()
        result = method(*args, **kwds)
        time_taken = datetime.datetime.now() - begin
        LOG.info(f'Finished method {method.__name__} with params {args} in {time_taken}.')
        return result

    return wrapper


def log_endpoint(method):
    """
    This decorator log api methods with its args and body.
    """

    @functools.wraps(method)
    def wrapper(*args, **kwds):
        LOG.info(f'API endpoint {request.full_path} called.\nArgs: {request.args}.\nData {request.data}.\nJson {request.json}.\nForm {request.form}')
        begin = datetime.datetime.now()
        result = method(*args, **kwds)
        time_taken = datetime.datetime.now() - begin
        LOG.info(f'Finished endpoint execution {method.__name__} in {time_taken}.\nResult: {result}.')
        return result

    return wrapper


def jwt_decode(token, secret):
    try:
        payload = jwt.decode(token, secret)
    except jwt.InvalidTokenError as e:
        LOG.info("Invalid token {}".format(str(e)))
        raise Forbidden()

    return payload


def jwt_encode(payload, secret):
    return jwt.encode(payload, secret).decode('utf-8')


def is_jwt(jwt_s):
    if jwt_s.find(".") == -1:
        return False
    header, unsigned_token, signature = jwt_s.split(".")
    return unsigned_token != '' and header != '' and signature != ''