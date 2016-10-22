import logging
import common.micro_webapp2 as micro_webapp2
from common.constants import Error
from handlers import BaseHandler, user_authenticate
app = micro_webapp2.WSGIApplication()

@app.api(r'/example')
class MainHandler(BaseHandler):
    def get(self, main_id=None):
        if not main_id:
            main_id = 'Hello, World!'
        test = {'main': main_id}
        self.res_json(test)
