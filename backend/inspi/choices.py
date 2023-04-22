from django.db import models
from django.utils.translation import gettext_lazy as _


class OptionType(models.IntegerChoices):
    LIKE = 1, _('Like'),
    DISLIKE = -1, _('Dislike')
