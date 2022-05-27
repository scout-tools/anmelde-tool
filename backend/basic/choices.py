from django.db import models
from django.utils.translation import gettext_lazy as _


class TravelType(models.TextChoices):
    Train = 'T', _('Bahn')
    Bus = 'B', _('Reisebus')
    Car = 'C', _('PKW')
    Other = 'O', _('Sonstiges')


class TravelSlots(models.TextChoices):
    Before = 'B', _('Früher')
    Early = 'E', _('16:00-18:00')
    Normal = 'N', _('18:00-20:00')
    Late = 'L', _('20:00-22:00')
    SuperLate = 'SL', _('22:00-24:00')
    Other = 'O', _('Noch Später')


class DescriptionType(models.TextChoices):
    FAQ = 'FAQ', _('FAQ')
    Privacy = 'P', _('Datenschutz')


class StateChoices(models.TextChoices):
    BW = 'BW', _('Baden-Württemberg')
    BY = 'BY', _('Bayern')
    BE = 'BE', _('Berlin')
    BB = 'BB', _('Brandenburg')
    HB = 'HB', _('Bremen')
    HH = 'HH', _('Hamburg')
    HE = 'HE', _('Hessen')
    MV = 'MV', _('Mecklenburg-Vorpommern')
    NI = 'NI', _('Niedersachsen')
    NW = 'NW', _('Nordrhein-Westfalen')
    RP = 'RP', _('Rheinland-Pfalz')
    SL = 'SL', _('Saarland')
    SN = 'SN', _('Sachsen')
    ST = 'ST', _('Sachsen-Anhalt')
    SH = 'SH', _('Schleswig-Holstein')
    TH = 'TH', _('Thüringen')
