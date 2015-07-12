from rest_framework import status
from rest_framework.exceptions import APIException


class BraintreeAPIException(APIException):
    status_code = status.HTTP_502_BAD_GATEWAY
    default_detail = 'A braintree error occurred.'


class TimeOverlapException(APIException):
    status_code = status.HTTP_409_CONFLICT
