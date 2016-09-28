import logging
import common.micro_webapp2 as micro_webapp2
from common.constants import Error
from handlers import BaseHanler
app = micro_webapp2.WSGIApplication()

@app.routes(['/', '/example', r'/example/<main_id>'])
class MainHandler(BaseHanler):
    def get(self, main_id=None):
        if not main_id:
            main_id = 'Hello, World!'
        test = {'main': main_id}
        self.res_json(test)
