import webapp2
import logging
import json
class BaseHanler(webapp2.RequestHandler):
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
            self.res(json.dumps(content), status)
        else:
            err_msg = 'content is not dict'
            logging.error(err_msg)
            self.res_error('content is not dict')
