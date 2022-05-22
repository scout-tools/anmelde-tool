from django.db import models
from django.utils.translation import gettext_lazy as _


class RegistrationTypeGroup(models.TextChoices):
    """
    No = No group registration allowed
    Optional = Group registration possible
    Required = Group registration is required => single registration can be only attached or not allowed at all
    """
    No = 'N', _('Nicht erlaubt')
    Optional = 'O', _('Optional')
    Required = 'R', _('Erforderlich')


class RegistrationTypeSingle(models.TextChoices):
    """
    No = No single person registrations allowed
    Attached = A single persons' registration has to be attached to a group registration
    Mixed = A single persons' registration can be attached to a group registration but is not a must
    External = Only standalone single persons' registrations allowed
    """
    No = 'N', _('Nicht erlaubt')
    Attached = 'A', _('Angefügt')
    Mixed = 'M', _('Gemischt')
    External = 'E', _('Extern')


class Gender(models.TextChoices):
    Male = 'M', _('Männlich')
    Female = 'F', _('Weiblich')
    Divers = 'D', _('Divers')
    Nothing = 'N', _('Keine Angabe')


class ParticipantActionConfirmation(models.TextChoices):
    Nothing = 'N', _('Nichts')
    Delete = 'D', _('Abmelden')
    AddFromExisting = 'AE', _('Anmelden von deaktivierten Teilnehmern'),
    AddCompletyNew = 'AN', _('Anmelden von neuen Teilnehmern'),


class LeaderTypes(models.TextChoices):
    KeineFuehrung = 'N', _('Kein Amt')
    StammesFuehrung = 'StaFue', _('Stammesführung')
    SippenFuehrung = 'SiFue', _('Sippenführung')
    RoverrundenFuehrung = 'RoFue', _('Roverrundenführung'),
    Meutenfuehrung = 'MeuFue', _('Meutenführung')


class FileGenerationStatus(models.TextChoices):
    Queued = 'Q', _('In der Warteschlange.')
    Processing = 'P', _('Dokument wird erstellt.')
    FinishedSuccessfull = 'FS', _('Dokument erfolgreich erstellt.')
    FinishedFailed = 'FF', _('Dokumenten Erstellung Fehlgeschlagen.')


class FileType(models.TextChoices):
    Kjp = 'K', _('KJP Liste')
    ParticipantList = 'P', _('Teilnehmerliste')


class FileExtension(models.TextChoices):
    Excel = 'E', _('Excel')
    PDF = 'P', _('PDF')