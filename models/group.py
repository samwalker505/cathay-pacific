from google.appengine.ext import ndb
from models import BaseModel
from models.message import Message
class Group(BaseModel):
    owner = ndb.KeyProperty()
    name = ndb.StringProperty()
    members = ndb.KeyProperty(repeated=True)
    pending_members = ndb.KeyProperty(repeated=True)
