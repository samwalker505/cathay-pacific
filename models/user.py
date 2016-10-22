import logging
from google.appengine.ext import ndb
from models import BaseModel

class AccessLevel(object):
    NORMAL = 1
    ADMIN = 10
    SUPER_ADMIN = 100

class FacebookProperty(ndb.Model):
    profile_pic = ndb.StringProperty()
    email = ndb.StringProperty()
    name = ndb.StringProperty()
    owner = ndb.KeyProperty()

class Facebook(FacebookProperty):

    @classmethod
    def connect_fb(cls, fat):
        url = 'https://graph.facebook.com/v2.7/me?fields=picture%2Cname%2Cemail&access_token={}'.format(fat)
        from google.appengine.api import urlfetch
        r = urlfetch.fetch(url)
        if r.status_code != 200:
            logging.debug(r.content)
            return None
        import json
        fb_result = json.loads(r.content)
        fb = cls.get_or_insert(fb_result['id'], profile_pic=fb_result['picture']['data']['url'], name=fb_result['name'], email=fb_result['email'])
        return fb

class UserProperty(ndb.Model):
    email = ndb.StringProperty()
    firstname = ndb.StringProperty()
    lastname = ndb.StringProperty()
    password = ndb.StringProperty()
    access_level = ndb.IntegerProperty(default=AccessLevel.NORMAL)
    nationality = ndb.KeyProperty()
    date_of_birth = ndb.DateTimeProperty()
    passport_number = ndb.StringProperty()
    visa_number = ndb.StringProperty()
    facebook = ndb.StructuredProperty(FacebookProperty)

class User(UserProperty, BaseModel):
    name = ndb.ComputedProperty(lambda self: '{} {}'.format(self.firstname if self.firstname else '', self.lastname if self.lastname else '').strip())

    def to_dict(self, include=None, exclude=None):
        d = super(User, self).to_dict(include, exclude)
        del d['password']
        return d


class Secret(BaseModel):
    secret = ndb.StringProperty()
    owner = ndb.KeyProperty()
