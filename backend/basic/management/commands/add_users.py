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
            user_2 = UserModel.objects.create_user('joto@dpbm.de', password='joto')
            user_2.is_superuser = True
            user_2.is_staff = True
            user_2.save()

        if not UserModel.objects.filter(username='daniel@hratuga.de').exists():
            user_3 = UserModel.objects.create_user('daniel@hratuga.de', password='daniel')
            user_3.is_superuser = False
            user_3.is_staff = True
            user_3.save()

        if not UserModel.objects.filter(username='caro@mittelerde.de').exists():
            user_4 = UserModel.objects.create_user('caro@mittelerde.de', password='caro')
            user_4.is_superuser = False
            user_4.is_staff = False
            user_4.save()

        if not UserModel.objects.filter(username='many@dpvonline.de').exists():
            user_5 = UserModel.objects.create_user('many@dpvonline.de', password='many')
            user_5.is_superuser = False
            user_5.is_staff = True
            user_5.save()

        if not UserModel.objects.filter(username='kai@dpv.de').exists():
            user_5 = UserModel.objects.create_user('kai@dpv.de', password='kai')
            user_5.is_superuser = False
            user_5.is_staff = False
            user_5.save()

        if not UserModel.objects.filter(username='dummy@dpv.de').exists():
            user_6 = UserModel.objects.create_user('dummy@dpv.de', password='testuser123')
            user_6.is_superuser = False
            user_6.is_staff = False
            user_6.save()

        if not UserModel.objects.filter(username='hagi@hratuga.de').exists():
            user_7 = UserModel.objects.create_user('hagi@hratuga.de', password='hagi1234')
            user_7.is_superuser = False
            user_7.is_staff = True
            user_7.save()

        if not UserModel.objects.filter(username='tonibaer97@gmail.com').exists():
            user_8 = UserModel.objects.create_user('tonibaer97@gmail.com', password='toni')
            user_8.is_superuser = False
            user_8.is_staff = False
            user_8.save()

        if not UserModel.objects.filter(username='kethe@pbn.de').exists():
            user = UserModel.objects.create_user('kethe@pbn.de', password='kethe')
            user.is_superuser = False
            user.is_staff = False
            user.save()

        if not UserModel.objects.filter(username='hagi@superadmin.de').exists():
            user = UserModel.objects.create_user('hagi@superadmin.de', password='hagi1234')
            user.is_superuser = True
            user.is_staff = True
            user.save()

        if not UserModel.objects.filter(username='hagi-kasse@bundesfahrt.de').exists():
            user = UserModel.objects.create_user('hagi-kasse@bundesfahrt.de', password='hagi1234')
            user.is_superuser = False
            user.is_staff = True
            user.save()

        if not UserModel.objects.filter(username='hagi-lagerleitung@bundesfahrt.de').exists():
            user = UserModel.objects.create_user('hagi-lagerleitung@bundesfahrt.de', password='hagi1234')
            user.is_superuser = False
            user.is_staff = True
            user.save()

        if not UserModel.objects.filter(username='hagi-lagerleitung@dpv.de').exists():
            user = UserModel.objects.create_user('hagi-lagerleitung@dpv.de', password='hagi1234')
            user.is_superuser = False
            user.is_staff = True
            user.save()

        if not UserModel.objects.filter(username='hagi-kueche@dpv.de').exists():
            user = UserModel.objects.create_user('hagi-kueche@dpv.de', password='hagi1234')
            user.is_superuser = False
            user.is_staff = True
            user.save()

        if not UserModel.objects.filter(username='hagi-kueche@keinerechte.de').exists():
            user = UserModel.objects.create_user('hagi-kueche@keinerechte.de', password='hagi1234')
            user.is_superuser = False
            user.is_staff = True
            user.save()

        print('user created')
