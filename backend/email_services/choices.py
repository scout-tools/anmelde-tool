from django.db import models
from django.utils.translation import gettext_lazy as _


class EmailType(models.TextChoices):
    StandardEmail = 'StandardEmail', _('Allgemeine Email')
    EventCreated = 'EventCreated', _('Event erstellt')
    EventUpdated = 'EventUpdated', _('Event verändert')
    RegistrationCreated = 'RegistrationCreated', _('Registrierung erstellt')
    RegistrationUpdated = 'RegistrationUpdated', _('Registrierung verändert'),
    RegistrationReminder = 'RegistrationReminder', _('Bestätigungs errinerung'),
    RegistrationAccepted = 'RegistrationAccepted', _('Registrierungsbestätigung'),
    PaymentReminder = 'PaymentReminder', _('Bezahlungserrinnerung'),
