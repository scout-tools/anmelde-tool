from django.db import models
from django.contrib.auth.models import User
from basic.models import ScoutHerarchy
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserExtended(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    password_date = models.DateTimeField(auto_now=True)
    scoutOrganisation = models.ForeignKey(
        ScoutHerarchy, on_delete=models.PROTECT, null=True, blank=True)
    mobileNumber = models.CharField(max_length=20, blank=True)
    scoutName = models.CharField(max_length=20, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserExtended.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userextended.save()
