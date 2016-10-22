import logging
import json
import webapp2
from common.constants import Error
from handlers import BaseHandler, user_authenticate
from models.trip import Country


class MainHandler(webapp2.RequestHandler):
    def get(self):
        f = open('country.json', 'r')
        result = json.loads(f.readline())
        for key, val in result.iteritems():
            Country.get_or_insert(key, code=key, name=val)
        self.response.write('ok')
app = webapp2.WSGIApplication([
  (r'/api/v1/init_countries', MainHandler),
])
