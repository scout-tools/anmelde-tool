from rest_framework.exceptions import APIException


class GroupAlreadyRegistered(APIException):
    status_code = 403
    default_detail = 'Your group is already registered'
    default_code = 'already_registered'


class NotResponsible(APIException):
    status_code = 403
    default_detail = 'An registration already exists, but you are not responsible'
    default_code = 'already_registered'


class SingleAlreadyRegistered(APIException):
    status_code = 403
    default_detail = "You're already registed"
    default_code = 'already_registered'


class SingleGroupNotAllowed(APIException):
    status_code = 403
    default_detail = "You already have a registation, please edit this one"
    default_code = 'already_registered'


class WrongRegistrationFormat(APIException):
    status_code = 405
    default_detail = "You're regisration contains information which does not fit to the event"
    default_code = 'missleading_information'


class RegistrationNotSupported(APIException):
    status_code = 501
    default_detail = "Attached registrations are currently not implemented"
    default_code = 'no_attached_registrations'


class WrongEventCode(APIException):
    status_code = 403
    default_detail = "Your your typed in code does not match the event code"
    default_code = 'wrong_code'


class WrongUrl(APIException):
    status_code = 400
    default_detail = "For single/group registrations use the correct url"
    default_code = 'wrong_url'


class TooEarly(APIException):
    status_code = 405
    default_detail = "The registration hasn't started yet!"
    default_code = 'too_early'


class TooLate(APIException):
    status_code = 405
    default_detail = "The registration is over!"
    default_code = 'too_late'
