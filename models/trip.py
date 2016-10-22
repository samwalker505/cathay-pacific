from google.appengine.ext import ndb
from models import BaseModel
from models.user import UserProperty

class Country(BaseModel):
    name = ndb.StringProperty()
    code = ndb.StringProperty()

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
