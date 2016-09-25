import logging
import common.micro_webapp2 as micro_webapp2

from models.user import User
from handlers import BaseHanler

app = micro_webapp2.WSGIApplication()

@app.route('/users')
class UsersHandler(BaseHanler):
    def get(self):
        self.response.write('Testing')

    def post(self):
        user_dict = {
            'email': 'samwalker505@gmail.com',
            'password': '123456',
            'name': 'sam',
            'access_level':1
        }
        user = User.create(user_dict)
        self.res_json(user.to_dict())


@app.route('/users/<user_id>')
class UserHandler(BaseHanler):
    pass
