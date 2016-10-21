import logging

import common.micro_webapp2 as micro_webapp2
from common.constants import Error

from models.trip import Trip
from handlers import BaseHandler, user_authenticate
app = micro_webapp2.WSGIApplication()

@app.api('/trips')
class TripsHandler(BaseHandler):

    @user_authenticate
    def get(self):
        result = self.query(Trip, filters=[Trip.owner==self.user.key])
        return self.res_json(result)

    @user_authenticate
    def post(self):
        allow_attrs = ['name', 'flight_number_to', 'flight_number_back', 'foreign_address', 'destination', 'last_visit_country', 'next_visit_country', 'duration']
        params = {k:v for k, v in self.json_body.iteritems() if k in allow_attrs}
        params['owner'] = self.user.key
        trip = Trip.create(params)
        return self.res_json(trip.to_dict())
