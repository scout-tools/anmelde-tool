from django.utils.encoding import force_str
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
    default_detail = "Du bist bereits Registriert."
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


class WrongRegistrationFormatGroup(APIException):
    status_code = 405
    default_detail = "Bei diesem Event können sich keine Gruppen registrieren."
    default_code = 'missleading_information'


class WrongRegistrationFormatSingle(APIException):
    status_code = 405
    default_detail = "Bei diesem Event können sich keine Einzelpersonen registrieren."
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


class WrongEventCodeForGroup(APIException):
    status_code = 403
    default_detail = "Dein eingegebener Code für eine Gruppenanmeldung ist leider nicht Korrekt!"
    default_code = 'wrong_code'


class WrongEventCodeForSingle(APIException):
    status_code = 403
    default_detail = "Dein eingegebener Code für eine Einzelanmeldung ist leider nicht Korrekt!"
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


class ModuleRequired(APIException):
    status_code = 405
    default_detail = "Du kannst dieses Modul nicht löschen, da es ein Pflichtmodul ist."
    default_code = 'required_module'


class EatHabitTooLong(APIException):
    status_code = 400
    default_detail = "Dein Eingegebener Essenswunsch ist zu lang, bitte jeden Wunsch einzeln angeben (max 100 Zeichen)."
    default_code = 'too_long'


class EndBeforeStart(APIException):
    status_code = 400
    default_detail = "Deine Fahrt fängt an nachdem es beendet ist."
    default_code = 'wrong_order'


class StartBeforeLastChange(APIException):
    status_code = 400
    default_detail = "Es dürfen noch Daten geändert werden, nachdem die Fahrt gestartet ist."
    default_code = 'wrong_order'


class LastChangeBeforeRegistrationDeadline(APIException):
    status_code = 400
    default_detail = "Das Datum der letzten Änderungen muss gleich oder später dem Anmeldeschluss sein."
    default_code = 'wrong_order'


class RegistrationDeadlineBeforeRegistrationStart(APIException):
    status_code = 400
    default_detail = "Der Anmeldeschluss liegt vor dem Anmeldestart."
    default_code = 'wrong_order'


class WrongQueryParams(APIException):
    status_code = 400
    default_detail = "Deine Anfrage ist nicht vollständig."
    default_code = 'wrong_query_params'


class EventNotFound(APIException):
    status_code = 404
    default_detail = "Das Event mit der ID {event_id} konnte nicht gefunden werden. " \
                     "Bitte überprüfe ob der Link richtig kopiert wurde/eingetippt wurde, " \
                     "andernfalls wende dich bitte(!) an die Administratoren und beschreibe das Problem."
    default_code = 'not_found'

    def __init__(self, event_id, detail=None, code=None):
        if detail is None:
            detail = force_str(self.default_detail).format(event_id=event_id)
        super().__init__(detail, code)


class ScoutHierarchyChildModelNotFound(APIException):
    status_code = 404
    default_detail = "Zu deinem Bund {bund} konnten wir leider keine Stämme berechnen," \
                     " um die dazugehörigen Registrierungen zu filtern. " \
                     "Bitte(!) wende dich an die Administratoren und beschreibe das Problem."
    default_code = 'not_found'

    def __init__(self, bund, detail=None, code=None):
        if detail is None:
            detail = force_str(self.default_detail).format(bund=bund)
        super().__init__(detail, code)


class SomethingNotFound(APIException):
    status_code = 404
    default_detail = "Das {sth} konnte leider nicht gefunden werden. " \
                     "Bitte(!) wende dich an die Administratoren und beschreibe das Problem."
    default_code = 'not_found'

    def __init__(self, sth, detail=None, code=None):
        if detail is None:
            detail = force_str(self.default_detail).format(sth=sth)
        super().__init__(detail, code)


class RequiredGroupNotFound(APIException):
    status_code = 404
    default_detail = "Die Berechtigung {permission} konnte leider nicht gefunden werden." \
                     "Bitte(!) wende dich an die Administratoren und beschreibe das Problem."
    default_code = 'not_found'

    def __init__(self, permission, detail=None, code=None):
        if detail is None:
            detail = force_str(self.default_detail).format(permission=permission)
        super().__init__(detail, code)


class RegistrationNotFound(APIException):
    status_code = 404
    default_detail = "Die Registrierung {registration} konnte leider nicht gefunden werden. " \
                     "Bitte überprüfe ob der Link richtig kopiert wurde/eingetippt wurde, " \
                     "andernfalls wende bitte(!) dich an die Administratoren und beschreibe das Problem."
    default_code = 'not_found'

    def __init__(self, registration, detail=None, code=None):
        if detail is None:
            detail = force_str(self.default_detail).format(registration=registration)
        super().__init__(detail, code)
