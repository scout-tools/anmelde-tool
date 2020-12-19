from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'add users'

    def handle(self, *args, **options):
        UserModel = get_user_model()

        if not UserModel.objects.filter(username='robert@hratuga.de').exists():
            user = UserModel.objects.create_user(
                'robert@hratuga.de', password='robert')
            user.is_superuser = True
            user.is_staff = True
            user.save()

        if not UserModel.objects.filter(username='daniel@hratuga.de').exists():
            user = UserModel.objects.create_user(
                'daniel@hratuga.de', password='daniel')
            user.is_superuser = False
            user.is_staff = True
            user.save()

        if not UserModel.objects.filter(username='caro@mittelerde.de').exists():
            user = UserModel.objects.create_user(
                'caro@mittelerde.de', password='caro')
            user.is_superuser = False
            user.is_staff = False
            user.save()

        if not UserModel.objects.filter(username='many@dpv.de').exists():
            user = UserModel.objects.create_user(
                'many@dpv.de', password='many')
            user.is_superuser = False
            user.is_staff = False
            user.save()
