import jwt
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
    HASH = '9ac696e7bbfd0ac3ec6e94933485b7c2'
    user_info = ndb.StructuredProperty(UserProperty)
    owner = ndb.KeyProperty()
    title = ndb.StringProperty()
    flight_number_to = ndb.StringProperty()
    flight_number_back = ndb.StringProperty()
    foreign_address = ndb.StringProperty()
    destination = ndb.KeyProperty()
    last_visit_country = ndb.KeyProperty()
    next_visit_country = ndb.KeyProperty()
    from_date = ndb.DateTimeProperty()
    to_date = ndb.DateTimeProperty()

    def gen_token(self):
        t = jwt.encode({'uid': self.key.id()}, Trip.HASH, algorithm='HS256')
        return t

    def validate_token(self, token):
        result = jwt.decode(token, Trip.HASH, algorithms=['HS256'])
        return True if result and result['uid'] == self.key.id() else False

    def to_dict(self, include=None, exclude=None):
        d = super(Trip, self).to_dict(include, exclude)
        for key in ['password', 'access_level', 'mark_deleted']:
            if d.get('user_info') and d['user_info'].get(key):
                del d['user_info'][key]

        t = self.gen_token()
        d['access_token'] = t
        return d
