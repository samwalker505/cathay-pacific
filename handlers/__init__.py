import webapp2
import logging
import json

from common.json_encoder import JSONEncoder
class BaseHanler(webapp2.RequestHandler):

    def __init__(self, request, response):
        self.json_body = {}
        self.initialize(request, response)

    def dispatch(self):
        if self.request.headers['Content-Type'].split(';')[0] == 'application/json':
            logging.debug('Content-Type: json')
            self.json_body = json.loads(self.request.body)
        super(BaseHanler, self).dispatch()

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
