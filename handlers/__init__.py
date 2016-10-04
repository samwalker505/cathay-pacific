#!
import webapp2
import logging
import json

from common.json_encoder import JSONEncoder
import common.config as config

def user_authenticate(func):
    def func_wrapper(self, *args, **kwargs):
        token = self.request.headers.get(config.HEADER_ACCESS_TOKEN)
        logging.debug('Token: {}'.format(token))
        tokenArr = token.split('::')
        if not token or len(tokenArr)< 2:
            self.abort(403)

        import jwt
        from models.user import User, Secret
        jwt_token = tokenArr[0]
        user_id = tokenArr[1]
        s = Secret.get_by_id(user_id)
        if not s:
            self.abort(403)
        decoded = jwt.decode(jwt_token, s.secret, algorithms=['HS256'])
        logging.debug('decoded: {}'.format(decoded))
        if decoded:
            self.user = s.owner.get()
            func(self, *args, **kwargs)
        else:
            self.abort(403)
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

    def options(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
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
        self.res_json(error, status)

    def res_json(self, content, status=200):
        if isinstance(content, dict):
            self.res(json.dumps(content, cls=JSONEncoder), status)
        else:
            err_msg = 'content is not dict'
            logging.error(err_msg)
            self.res_error('content is not dict')
