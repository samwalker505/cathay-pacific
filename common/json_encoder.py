from datetime import datetime
from google.appengine.ext import ndb
import json

class JSONEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        elif isinstance(o, ndb.Key):
            return o.id()

        return json.JSONEncoder.default(self, o)
