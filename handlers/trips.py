import logging
import jwt

import common.micro_webapp2 as micro_webapp2
from common.constants import Error
from common.util import Util

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
        else:
            user_info = params.get('user_info')
            date_of_birth = user_info.get('date_of_birth')
            nationality = user_info.get('nationality')
            c, k =  Country.get_by_code(nationality)

            if not c:
                self.res_error('ERROR_COUNTRY_NOT_ALLOWED')
            else:
                logging.debug('user_info nationality')
                params['user_info']['nationality'] = k

            if date_of_birth:
                params['user_info']['date_of_birth'] = Util.from_timestamp(params['user_info']['date_of_birth'])

        for key in ['from_date', 'to_date']:
            if params.get(key):
                params[key] = Util.from_timestamp(params[key])

        for key in ['last_visit_country', 'next_visit_country']:
            if params.get(key):
                c, k = Country.get_by_code(params.get(key))
                logging.debug(k)
                logging.debug(c)
                if not c:
                    return self.res_error('ERROR_COUNTRY_NOT_ALLOWED')
                else:
                    params[key] = k

        trip = Trip.create(params)
        d = trip.to_dict()
        t = trip.gen_token()
        d['access_token'] = t
        return self.res_json(d)

@app.api('/trips/<trip_id>')
class TripHandler(BaseHandler):
    pass
