import uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from basic.models import ScoutHierarchy


class EmailNotificationType(models.TextChoices):
    """
    Choices a user can select, how often he wants to receive emails"
    """
    FULL = 'Full', _('Alles')
    DAILY = 'Daily', _('täglich')
    WEEKLY = 'Weekly', _('Wöchentlich')
    IMPORTANT = 'Important', _('Nur wichtiges')


class UserExtended(models.Model):
    """
    Model containing additional information of a user
    """
    id = models.UUIDField(auto_created=True, primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    scout_organisation = models.ForeignKey(ScoutHierarchy, on_delete=models.PROTECT, null=True, blank=True)
    mobile_number = models.CharField(max_length=20, blank=True)
    scout_name = models.CharField(max_length=20, blank=True)
    dsgvo_confirmed = models.BooleanField(default=False)
    email_notifaction = models.CharField(max_length=10,
                                         choices=EmailNotificationType.choices,
                                         default=EmailNotificationType.FULL)
    sms_notifcation = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f'{self.user} - {self.scout_organisation}'

    def __repr__(self) -> str:
        return self.__str__()


# pylint: disable=unused-argument
@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance: get_user_model(), created, **kwargs):
    """
    @param sender: User
    @param instance: None, as no user exists at this time
    @param created: bool if a user is newly created
    @return: None
    When a user is created, automatically create an UserExtended instance and connect it to the newly created user
    """
    if created:
        UserExtended.objects.create(user=instance)


# pylint: disable=unused-argument
@receiver(post_save, sender=get_user_model())
def save_user_profile(sender, instance: get_user_model(), **kwargs):
    """
    @param sender: User
    @param instance: connected user
    @return: None
    When a user is saved, automatically save the connected UserExtended instance
    """
    instance.userextended.save()
