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

        if not UserModel.objects.filter(username='joto@dpbm.de').exists():
            user_2 = UserModel.objects.create(
                username='joto@dpbm.de', password='joto')
            user_2.is_superuser = False
            user_2.is_staff = False
            user_2.save()

        if not UserModel.objects.filter(username='daniel@hratuga.de').exists():
            user_3 = UserModel.objects.create(
                username='daniel@hratuga.de', password='daniel')
            user_3.is_superuser = False
            user_3.is_staff = True
            user_3.save()

        if not UserModel.objects.filter(username='caro@mittelerde.de').exists():
            user_4 = UserModel.objects.create(
                username='caro@mittelerde.de', password='caro')
            user_4.is_superuser = False
            user_4.is_staff = False
            user_4.save()

        if not UserModel.objects.filter(username='many@dpv.de').exists():
            user_5 = UserModel.objects.create(
                username='many@dpv.de', password='many')
            user_5.is_superuser = False
            user_5.is_staff = False
            user_5.save()

        if not UserModel.objects.filter(username='kai@dpv.de').exists():
            user_5 = UserModel.objects.create(
                username='kai@dpv.de', password='kai')
            user_5.is_superuser = False
            user_5.is_staff = False
            user_5.save()

        # lagerleitung
        user = User.objects.get(username='joto@dpbm.de')
        new_group = Group.objects.get_or_create(name='lagerleitung')
        user.groups.add(new_group[0].id)

        # kueche
        user = User.objects.get(username='caro@mittelerde.de')
        new_group = Group.objects.get_or_create(name='kueche')
        user.groups.add(new_group[0].id)

        # kasse
        user = User.objects.get(username='many@dpv.de')
        new_group = Group.objects.get_or_create(name='kasse')
        user.groups.add(new_group[0].id)

        # logistic
        user = User.objects.get(username='many@dpv.de')
        new_group = Group.objects.get_or_create(name='logistic')
        user.groups.add(new_group[0].id)

        # social_media
        user = User.objects.get(username='kai@dpv.de')
        new_group = Group.objects.get_or_create(name='social_media')
        user.groups.add(new_group[0].id)
