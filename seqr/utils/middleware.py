from django.utils.deprecation import MiddlewareMixin
import logging
import traceback

from seqr.views.utils.json_utils import create_json_response
from settings import DEBUG

logger = logging.getLogger()


class JsonErrorMiddleware(MiddlewareMixin):

    @staticmethod
    def process_exception(request, exception):
        if request.path.startswith('/api'):
            exception_json = {'message': str(exception.message)}
            traceback_message = traceback.format_exc()
            logger.error(traceback_message)
            if DEBUG:
                exception_json['traceback'] = traceback_message.split('\n')
            return create_json_response(exception_json, status=500)
        return None