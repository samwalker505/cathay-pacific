import logging
import md5
from validate_email import validate_email
from google.appengine.ext import ndb
import webapp2

from models.user import User, Facebook
from models.email import Email
from models.trip import Country
from handlers import BaseHandler, user_authenticate
from common.constants import Error
from common.util import Util

import common.micro_webapp2 as micro_webapp2
app = micro_webapp2.WSGIApplication()

@app.api('/users')
class UsersHandler(BaseHandler):

    @user_authenticate
    def get(self):
        logging.debug('enter user get')
        import inspect
        logging.debug(self.user.to_dict())
        return self.res_json(self.user.to_dict())

    def connect_fb(self):
        fb = Facebook.connect_fb(self.json_body['fat'])
        if not fb:
            return self.res_error('connect facebook error')

        e = Email.get_or_insert(fb.email)

        # email will have owner if registered
        if e.owner:
            # connect with existing user
            user = e.owner.get()
            user.facebook = fb
            user.put()
        else:
            create_dict = {
                'email':fb.email,
                'firstname':fb.name,
                'facebook':fb
            }
            user = User.create(create_dict)
            e.owner = user.key
            e.put()

        fb.owner = user.key
        fb.put()
        return self.res_json(user.to_dict())


    def post(self):
        if 'fat' in self.json_body:
            return self.connect_fb()

        email = self.json_body.get('email')
        if not (email and validate_email(email)):
            return self.res_error(Error.INVALID_EMAIL)
        e = Email.get_or_insert(email)
        # email will have owner if registered
        if e.owner:
            return self.res_error(Error.EMAIL_REGISTERED)

        password = self.json_body.get('password')
        if not password:
            logging.debug('password: {}'.format(password))
            return self.res_error(Error.NO_PASSWORD)

        name = self.json_body.get('name')
        name = name if name else email.split('@')[0]

        create_dict = {
            'email': email,
            'password': md5.new(password).hexdigest(),
            'firstname': name
        }
        user = User.create(create_dict)
        e.owner = user.key
        e.put()
        return self.res_json(user.to_dict())

    @user_authenticate
    def put(self):
        allow_attrs = User.UPDATE_FIELDS
        params = {k:v for k, v in self.json_body.iteritems() if k in allow_attrs}
        user = self.user
        date_of_birth = params.get('date_of_birth')
        logging.debug(date_of_birth)
        if date_of_birth:

            params['date_of_birth'] = Util.from_timestamp(date_of_birth)

        gender = params.get('gender')
        if gender and gender not in ['male', 'female', 'transgender']:
            return self.res_error('ERROR_GENDER_NOT_ALLOWED')

        nationality = params.get('nationality')
        if nationality:
            country, key = Country.get_by_code(nationality)
            if not country:
                return self.res_error('ERROR_COUNTRY_NOT_ALLOWED')
            params['nationality'] = key

        user.update(params)
        return self.res_json(user.to_dict())



@app.api('/users/<user_id>')
class UserHandler(BaseHandler):

    def get(self, user_id):
        logging.debug('user_id')
        user = User.get_by_id(long(user_id))
        if user:
            return self.res_json(user.to_dict())
        else:
            return self.res_error(Error.NO_USER)
