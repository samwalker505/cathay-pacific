#!
import webapp2
import logging
import json

from common.json_encoder import JSONEncoder
import common.config as config

import jwt
from models.user import User, Secret

def get_secret(token):
    logging.debug('Token: {}'.format(token))
    if not token:
        return None, None
    else:
        tokenArr = token.split('::')
        if len(tokenArr) < 2:
            return None, None

        jwt_token = tokenArr[0]
        user_id = tokenArr[1]
        return Secret.get_by_id(user_id), jwt_token

def get_user(token):
    s, jwt_token = get_secret(token)
    if not s:
        return None
    decoded = jwt.decode(jwt_token, s.secret, algorithms=['HS256'])
    logging.debug('decoded: {}'.format(decoded))
    if decoded:
        return s.owner.get()
    else:
        return None
    return None

def user_authenticate(func):
    def func_wrapper(self, *args, **kwargs):
        token = self.request.headers.get(config.HEADER_ACCESS_TOKEN)
        user = get_user(token)
        if user:
            self.user = user
            func(self, *args, **kwargs)
        else:
            self.abort(403)
    return func_wrapper

def get_current_user(func):
    def func_wrapper(self, *args, **kwargs):
        token = self.request.headers.get(config.HEADER_ACCESS_TOKEN)
        self.user = get_user(token)
        func(self, *args, **kwargs)
    return func_wrapper

class BaseHanler(webapp2.RequestHandler):

    def __init__(self, request, response):
        self.json_body = {}
        self.initialize(request, response)

    def dispatch(self):
        if self.request.headers['Content-Type'].split(';')[0] == 'application/json':
            logging.debug('Content-Type: json')
            self.json_body = json.loads(self.request.body)
        try:
            super(BaseHanler, self).dispatch()
        except Exception as e:
            logging.debug(e)

    def res(self, content='no content', status=200, content_type='application/json'):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.set_status(status)
        self.response.headers['Content-Type'] = content_type
        self.response.write(content)

    def res_error(self, content, status=400):
        error = {
            'code': status,
            'message': content
        }
        self.res_json(error, status)

    def res_json(self, content, status=200):
        if isinstance(content, dict):
            self.res(json.dumps(content, cls=JSONEncoder), status)
        else:
            err_msg = 'content is not dict'
            logging.error(err_msg)
            self.res_error('content is not dict')
