from google.appengine.ext import ndb
from models import BaseModel

class AccessLevel(object):
    NORMAL = 1
    ADMIN = 10
    SUPER_ADMIN = 100

class UserProperty(ndb.Model):
    email = ndb.StringProperty()
    password = ndb.StringProperty()
    name = ndb.StringProperty()
    access_level = ndb.IntegerProperty(default=AccessLevel.NORMAL)

class User(UserProperty, BaseModel):

    def to_dict(self, include=None, exclude=None):
        d = super(User, self).to_dict(include, exclude)
        del d['password']
        return d
