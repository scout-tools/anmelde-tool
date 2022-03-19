from basic.models import ScoutHierarchy
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
import uuid


class EmailNotificationType(models.TextChoices):
    Full = 'Full', _('Full')
    Daily = 'Daily', _('Daily')
    OnlyImportant = 'Important', _('Important')


class UserExtended(models.Model):
    id = models.UUIDField(auto_created=True, primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    scout_organisation = models.ForeignKey(ScoutHierarchy, on_delete=models.PROTECT, null=True, blank=True)
    mobile_number = models.CharField(max_length=20, blank=True)
    scout_name = models.CharField(max_length=20, blank=True)
    dsgvo_confirmed = models.BooleanField(default=False)
    email_notifaction = models.CharField(max_length=10,
                                         choices=EmailNotificationType.choices,
                                         default=EmailNotificationType.Full)
    sms_notifcation = models.BooleanField(default=True)

    def __str__(self):
        return "{} - {}".format(self.user, self.scout_organisation)

    def __repr__(self):
        return self.__str__()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserExtended.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userextended.save()
