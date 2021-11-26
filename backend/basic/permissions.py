from rest_framework import status, exceptions


class NoRegistationId(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "No Registration id given"
