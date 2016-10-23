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
            return func(self, *args, **kwargs)
        else:
            self.abort(403)
    return func_wrapper

def get_current_user(func):
    def func_wrapper(self, *args, **kwargs):
        token = self.request.headers.get(config.HEADER_ACCESS_TOKEN)
        self.user = get_user(token)
        return func(self, *args, **kwargs)
    return func_wrapper

def output(func, output_format='json'):
    logging.debug('enter output')
    def func_wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        logging.debug(result)
        if output_format == 'json':
            return self.res_json(result)
    return func_wrapper



class BaseHandler(webapp2.RequestHandler):

    def __init__(self, request, response):
        self.json_body = {}
        self.initialize(request, response)


    def query(self, kls, per_page=1000, filters=[], order=None):
        from google.appengine.datastore.datastore_query import Cursor
        cursor = Cursor.from_websafe_string(str(self.request.get('cursor')))
        query = kls.query()
        if filters:
            logging.debug('filters: {}'.format(filters))
            for f in filters:
                query = query.filter(f)
        if order:
            query = query.order(order)

        results, next_cursor, more = query.fetch_page(per_page, start_cursor=cursor)
        result = {
            'cursor': next_cursor,
            'results': [result.to_dict() for result in results],
            'count': query.count(),
            'more': more
        }

        return result

    def dispatch(self):
        content_type = self.request.headers.get('Content-Type')
        if content_type and content_type.split(';')[0] == 'application/json':
            logging.debug('Content-Type: json')
            self.json_body = json.loads(self.request.body)
        # don't indent it ....

        super(BaseHandler, self).dispatch()

    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        pass

    def options(self, *args, **kwargs):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, X-WALKER-ACCESS-TOKEN'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'

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
        return self.res_json(error, status)

    def res_json(self, content, status=200):
        logging.debug(content)
        if isinstance(content, dict):
            return self.res(json.dumps(content, cls=JSONEncoder), status)
        else:
            err_msg = 'res_json: content is not dict'
            logging.error(err_msg)
            return self.res_error('content is not dict')
