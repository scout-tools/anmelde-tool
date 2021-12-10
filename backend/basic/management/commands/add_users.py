from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, User


class Command(BaseCommand):
    help = 'add users'

    def handle(self, *args, **options):
        UserModel = get_user_model()

        if not UserModel.objects.filter(username='robert@hratuga.de').exists():
            user_1 = UserModel.objects.create_user('robert@hratuga.de', password='robert')
            user_1.is_superuser = True
            user_1.is_staff = True
            user_1.save()

        if not UserModel.objects.filter(username='dummy@dpv.de').exists():
            user_6 = UserModel.objects.create_user('dummy@dpv.de', password='dummy1234')
            user_6.is_superuser = False
            user_6.is_staff = True
            user_6.save()

        if not UserModel.objects.filter(username='hagi@hratuga.de').exists():
            user_7 = UserModel.objects.create_user('hagi@hratuga.de', password='hagi1234')
            user_7.is_superuser = True
            user_7.is_staff = True
            user_7.save()

        print('user created')
