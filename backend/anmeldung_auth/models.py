from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserExtended(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    password_date = models.DateTimeField(auto_now=True)


@receiver(post_save, sender=User, dispatch_uid='save_new_user_profile')
def save_profile(sender, instance, created, **kwargs):
    instance.userextended.save()


