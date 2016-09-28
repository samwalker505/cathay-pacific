import logging
import md5
from validate_email import validate_email

import common.micro_webapp2 as micro_webapp2
from models.user import User
from models.email import Email
from handlers import BaseHanler
from common.constants import Error
app = micro_webapp2.WSGIApplication()

@app.api('/users')
class UsersHandler(BaseHanler):

    def get(self):
        self.response.write('Testing')

    def post(self):
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

        create_dict = {
            'email': email,
            'password': md5.new(password).hexdigest()
        }
        user = User.create(create_dict)
        e.owner = user.key
        e.put()
        return self.res_json(user.to_dict())

@app.api(r'/users/<user_id>')
class UserHandler(BaseHanler):
    def get(self, user_id):
        logging.debug(user_id)
        user = User.get_by_id(long(user_id))
        if user:
            return self.res_json(user.to_dict())
        else:
            return self.res_error(Error.NO_USER)

@app.api(r'/users/<user_id>/photos')
class UserPhotoHandler(BaseHanler):
    def get(self, user_id):
        logging.debug(user_id)
        # user = User.get_by_id(long(user_id))
        self.res_json({user_id: 'photo'})
