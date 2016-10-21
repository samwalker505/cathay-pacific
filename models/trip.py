from google.appengine.ext import ndb
from models import BaseModel

class Trip(BaseModel):
    name = ndb.StringProperty()
    owner = ndb.KeyProperty()
    flight_number_to = ndb.StringProperty()
    flight_number_back = ndb.StringProperty()
    foreign_address = ndb.StringProperty()
    destination = ndb.StringProperty()
    last_visit_country = ndb.StringProperty()
    next_visit_country = ndb.StringProperty()
    duration = ndb.FloatProperty()
