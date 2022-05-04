from rest_framework.exceptions import APIException


class TooManySearchResults(APIException):
    status_code = 403
    default_detail = 'Zu viele Treffer.'
    default_code = 'too_many_results'


class NoSearchResults(APIException):
    status_code = 400
    default_detail = 'Keine Treffer.'
    default_code = 'no_results'

class NoSearchValue(APIException):
    status_code = 400
    default_detail = 'Bitte PLZ oder Ort eingeben.'
    default_code = 'no_query'
