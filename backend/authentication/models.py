import uuid
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from basic import models as basic_models

from event.choices import choices as event_choices

class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True

class BundesPostTextChoice(models.TextChoices):
    """
    Choices a user can select, how often he wants to receive emails"
    """
    NOTHING = 'nothing', _('Keine Bundespost')
    DIGITAL = 'digital', _('Nur Digital')
    DIGITAL_POST = 'digital_post', _('Digital und Post')
    POST = 'post', _('Nur per Post')

class Person(TimeStampMixin):
    """
    Model to save a natrual person with or without login
    """
    id = models.UUIDField(auto_created=True, primary_key=True, default=uuid.uuid4, editable=False)
    scout_name = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=100, default="")
    address = models.CharField(max_length=200, blank=True, null=True)
    address_supplement = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.ForeignKey(basic_models.ZipCode, on_delete=models.PROTECT, null=True, blank=True)
    scout_group = models.ForeignKey(basic_models.ScoutHierarchy, on_delete=models.PROTECT, null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    phone_number_verified = models.BooleanField(default=0)
    email = models.EmailField(null=True, blank=True)
    email_verified = models.BooleanField(default=0)
    bundespost = models.CharField(max_length=13, choices=BundesPostTextChoice.choices,
                                   default=BundesPostTextChoice.NOTHING)
    birthday = models.DateField(null=True, blank=True)
    tags = models.ManyToManyField(basic_models.AbstractAttribute, blank=True)
    gender = models.CharField(max_length=1, choices=event_choices.Gender.choices, default=event_choices.Gender.Nothing)
    active = models.BooleanField(default=False)
    person_verified = models.BooleanField(default=False)
    eat_habits = models.ManyToManyField(basic_models.EatHabit, blank=True)
    leader = models.CharField(max_length=6, choices=event_choices.LeaderTypes.choices,
                              default=event_choices.LeaderTypes.KeineFuehrung)
    scout_level = models.CharField(max_length=6, choices=event_choices.ScoutLevelTypes.choices,
                                   default=event_choices.ScoutLevelTypes.Unbekannt)
    owned_by = models.ManyToManyField(User, related_name='owners')
    created_by = models.ForeignKey(User, related_name='creator', on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.first_name} - {self.last_name} (self.scout_name)'

    def __repr__(self) -> str:
        return self.__str__()


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
    person = models.ForeignKey(Person, null=True, blank=True, on_delete=models.PROTECT)
    scout_organisation = models.ForeignKey(basic_models.ScoutHierarchy, on_delete=models.PROTECT, null=True, blank=True)
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
