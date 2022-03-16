from rest_framework.exceptions import APIException


class GroupAlreadyRegistered(APIException):
    status_code = 403
    default_detail = 'Dein Stamm ist bereits registriert.'
    default_code = 'already_registered'


class NotResponsible(APIException):
    status_code = 403
    default_detail = 'Dein Stamm ist registriert, aber du hast leider keine Befugnisse die Registrierung zu bearbeiten.'
    default_code = 'already_registered'


class SingleAlreadyRegistered(APIException):
    status_code = 403
    default_detail = "Du bist bereits Registriert"
    default_code = 'already_registered'


class SingleGroupNotAllowed(APIException):
    status_code = 403
    default_detail = "Bitte deine bestehende Registrierung bearbeiten anstatt eine neue anzulegen."
    default_code = 'already_registered'


class WrongRegistrationFormat(APIException):
    status_code = 405
    default_detail = "Deine zur Verfügung gestellten Informationen passen leider nicht zu den Einstellungen " \
                     "dieses Events, bitte wende dich an das Team."
    default_code = 'missleading_information'


class RegistrationNotSupported(APIException):
    status_code = 501
    default_detail = "Angefügte Registrierungen sind leider noch nicht Implementiert " \
                     "und stehen daher noch nicht zur Verfügung."
    default_code = 'no_attached_registrations'


class WrongEventCode(APIException):
    status_code = 403
    default_detail = "Dein eingegebener Code ist leider nicht Korrekt!"
    default_code = 'wrong_code'


class TooEarly(APIException):
    status_code = 405
    default_detail = "Die Registrierungsphase hat noch nicht begonnen!"
    default_code = 'too_early'


class TooLate(APIException):
    status_code = 405
    default_detail = "Die Registrierungsphase ist vorbei!"
    default_code = 'too_late'


class TooManyParticipants(APIException):
    status_code = 405
    default_detail = "Bitte melde erst alle Teilnehmer ab, da dies die Lagerleitung bestätigen musst."
    default_code = 'too_late'
