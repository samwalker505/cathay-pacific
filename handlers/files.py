import logging
import md5
from validate_email import validate_email

import webapp2

from handlers import get_current_user, BaseHanler
from common.constants import Error
from models.file import Image, File

class FilesHandler(BaseHanler):

    @get_current_user
    def post(self):
        logging.debug('enter post images')

        user = self.user if hasattr(self, 'user') else None
        data = self.request.POST.getall('file')

        if not data:
            return self.res_error('NO_DATA')

        file_type = self.request.get('file_type')
        if file_type not in ('file', 'image'):
            return self.res_error('Not allowed file_type: {}'.format(file_type))

        klass = Image if file_type == 'image' else File
        try:
            f = klass.add(data[0].file.read(), data[0].filename, user, file_type=file_type)
            return self.res_json(f.to_dict())
        except Exception as e:
            logging.debug(e)
            return self.res_error('file not allowed')

app = webapp2.WSGIApplication([
    (r'/files', FilesHandler),
])
