import logging
import md5
import time

import jwt

from handlers import BaseHandler
from common.constants import Error
from models.user import Secret, Facebook
from models.email import Email


import common.micro_webapp2 as micro_webapp2
app = micro_webapp2.WSGIApplication()

def gen_token(user):
    s = Secret.get_or_insert(str(user.key.id()))
    if not s.secret:
        s.secret = md5.new('{}:{}'.format(user.password, time.time())).hexdigest()
        s.owner = user.key
        s.put()

    payload = {
        'id': user.key.id(),
        'ts': time.time()
    }
    return '{}::{}'.format(jwt.encode(payload, s.secret, algorithm='HS256'), user.key.id())

def response_dict(user):
    token = gen_token(user)
    d = user.to_dict()
    d['access_token'] = token
    return d

@app.api('/tokens')
class TokensHandler(BaseHandler):
    def post(self):

        if 'fat' in self.json_body:
            fb = Facebook.connect_fb(self.json_body['fat'])
            if fb and fb.owner:
                return self.res_json(response_dict(fb.owner.get()))

        email = self.json_body.get('email')
        password = self.json_body.get('password')
        if not email or not password:
            return self.res_error(Error.NO_EMAIL_PASSWORD)

        email_log = Email.get_by_id(email)
        if email_log and email_log.owner:
            user = email_log.owner.get()
            if md5.new(password).hexdigest() != user.password:
                return self.res_error(Error.INVALID_PASSWORD, status=403)

            d = response_dict(user)
            return self.res_json(d)
        else:
            return self.res_error(Error.NO_USER)
