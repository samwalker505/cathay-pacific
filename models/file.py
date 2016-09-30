import cloudstorage as gcs
from google.appengine.ext import ndb
from models import BaseModel
from google.appengine.api import app_identity
from google.appengine.ext import blobstore
from google.appengine.api import images

class FileProperties(ndb.Model):
    owner = ndb.KeyProperty()
    name = ndb.StringProperty()
    gcs_path = ndb.StringProperty()
    url = ndb.StringProperty()
    blob_key = ndb.BlobProperty()

class File(FileProperties, BaseModel):
    @classmethod
    def upload_to_gcs(cls, data, filename=''):
        bucket_name = app_identity.get_default_gcs_bucket_name()
        path = '/{}/{}'.format(bucket_name, filename)
        gcs_file = gcs.open(path, 'w', options={'x-goog-acl': 'public-read'})
        gcs_file.write(data)
        gcs_file.close()
        blob_key = blobstore.create_gs_key('/gs'+path)
        return path, blob_key

    @classmethod
    def add(cls, data, filename='', owner=None):
        if not filename:
            import time
            filename = 'file_{}'.format(time.time())
        gcs_path, blob_key = cls.upload_to_gcs(data, filename)
        f = File(owner=owner.key if owner else None, name=filename, gcs_path=gcs_path, blob_key=blob_key)
        f.put()
        return f

class Image(File):
    @classmethod
    def add(cls, data, filename='', owner=None):
        if not filename.endswith(('.jpg','.jpeg','.gif','.png','.bmp','.ico')):
            raise Exception('Not image')
        f = super(Image, cls).add(data, filename, owner)
        f.url = images.get_serving_url(f.blob_key, secure_url=True)
        f.put()
        return f
