import logging
import md5
from validate_email import validate_email

import webapp2

import common.micro_webapp2 as micro_webapp2

from handlers import get_current_user, BaseHanler
from common.constants import Error
from models.file import Image
app = micro_webapp2.WSGIApplication()

@app.api('/images')
class ImagesHandler(BaseHanler):

    @get_current_user
    def post(self):
        logging.debug('enter post images')
        data = self.request.POST.getall('image')
        if not data:
            return self.res_error('NO_IMAGE')
        else:
            if hasattr(self, 'user'):
                user = self.user
            else:
                user = None
            try:
                image = Image.add(data[0].file.read(), data[0].filename, user)
                return self.res_json(image.to_dict())
            except Exception as e:
                logging.debug(e)
                return self.res_error('image not allowed')
