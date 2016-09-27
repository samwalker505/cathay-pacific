from google.appengine.ext import ndb
from models import BaseModel

class Email(BaseModel):
    owner = ndb.KeyProperty()
