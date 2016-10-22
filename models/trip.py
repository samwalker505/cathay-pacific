from google.appengine.ext import ndb
from models import BaseModel
from models.user import UserProperty

class Country(BaseModel):
    name = ndb.StringProperty()
    code = ndb.StringProperty()

    @classmethod
    def get_by_code(cls, codes):
        if isinstance(codes, list):
            key = [ndb.Key(cls, str(code)) for code in codes]
            result = ndb.get_multi(key)
        else:
            key = ndb.Key(cls, str(codes))
            result = key.get()
        return result, key

class Trip(BaseModel):

    user_info = ndb.StructuredProperty(UserProperty)
    owner = ndb.KeyProperty()
    flight_number_to = ndb.StringProperty()
    flight_number_back = ndb.StringProperty()
    foreign_address = ndb.StringProperty()
    destination = ndb.StringProperty()
    last_visit_country = ndb.StringProperty()
    next_visit_country = ndb.StringProperty()
    from_date = ndb.DateTimeProperty()
    to_date = ndb.DateTimeProperty()

    def to_dict(self, include=None, exclude=None):
        d = super(Trip, self).to_dict(include, exclude)
        del d['user_info']['password']
        del d['user_info']['access_level']
        del d['user_info']['mark_deleted']
        return d
