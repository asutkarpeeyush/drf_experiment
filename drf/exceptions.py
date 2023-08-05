from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler
from rest_framework import status
from datetime import datetime


class InvalidPersonDetailsException(APIException):
    default_detail = None
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, detail=None):
        super().__init__(detail, self.status_code)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response:
        response.data['status_code'] = response.status_code
        response.data['time'] = datetime.now()

    return response
