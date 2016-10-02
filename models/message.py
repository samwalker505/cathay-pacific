from google.appengine.ext import ndb
from models import BaseModel

class Message(BaseModel):
    sender = ndb.KeyProperty()
    content = ndb.TextProperty()
    msg_type = ndb.StringProperty(default='text')
    group = ndb.KeyProperty(kind='Group')
