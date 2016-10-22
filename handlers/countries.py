import logging
import common.micro_webapp2 as micro_webapp2
from common.constants import Error
from handlers import BaseHandler, user_authenticate
from models.trip import Country
app = micro_webapp2.WSGIApplication()

@app.api(r'/countries')
class CountriesHandler(BaseHandler):
    def get(self):
        result = self.query(Country)
        return self.res_json(result)
