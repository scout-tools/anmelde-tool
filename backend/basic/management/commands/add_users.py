from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'add users'

    def handle(self, *args, **options):
        UserModel = get_user_model()

        if not UserModel.objects.filter(username='robert_admin').exists():
            user_1 = UserModel.objects.create_user('robert_admin', password='robert1234')
            user_1.is_superuser = True
            user_1.is_staff = True
            user_1.save()

        if not UserModel.objects.filter(username='hagi_admin').exists():
            user_2 = UserModel.objects.create_user('hagi_admin', password='hagi1234')
            user_2.is_superuser = True
            user_2.is_staff = True
            user_2.save()

        print('user created')
