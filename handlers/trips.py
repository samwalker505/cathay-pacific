import logging

import common.micro_webapp2 as micro_webapp2
from common.constants import Error


from models.trip import Trip, Country
from handlers import BaseHandler, get_current_user, user_authenticate
app = micro_webapp2.WSGIApplication()

@app.api('/trips')
class TripsHandler(BaseHandler):
    @user_authenticate
    def get(self):
        result = self.query(Trip, filters=[Trip.owner==self.user.key])
        return self.res_json(result)

    @get_current_user
    def post(self):
        allow_attrs = ['flight_number_to', 'flight_number_back', 'foreign_address',
                        'destination', 'last_visit_country', 'next_visit_country',
                        'from_date', 'to_date', 'user_info']
        params = {k:v for k, v in self.json_body.iteritems() if k in allow_attrs}
        if self.user:
            params['user_info'] = self.user
            params['owner'] = self.user.key

        for key in ['last_visit_country, next_visit_country']:
            if params.get(key):
                c, k = Country.get_by_code(params.get(key))
                if not c:
                    return self.res_error('ERROR_COUNTRY_NOT_ALLOWED')
                else:
                    params[key] = k

        trip = Trip.create(params)
        return self.res_json(trip.to_dict())

@app.api('/trips/<trip_id>')
class TripHandler(BaseHandler):
    pass
