import random
from datetime import datetime, time
from django.contrib.auth import get_user_model
import pytz
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.utils import timezone

from event.choices.choices import ParticipantActionConfirmation
from event.models import RegistrationParticipant, Workshop, Event
from basic.models import StringAttribute, Message

User = get_user_model()


class Command(BaseCommand):
    help = 'make participants anonymous'

    def handle(self, *args, **options):
        for i, participant in enumerate(RegistrationParticipant.objects.all()):
            participant.scout_name = 'Teilnehmender'
            participant.first_name = 'Teilnehmender'
            participant.last_name = i
            participant.street = f'Straße {i}'
            participant.scout_group = None
            participant.phone_number = ''
            participant.email = ''
            participant.deactivated = False
            participant.needs_confirmation = ParticipantActionConfirmation.Nothing

            if participant.age:
                age = participant.age
            else:
                age = relativedelta(timezone.now(), participant.birthday).years

            age += random.randint(-2, 2)
            participant.age = age
            birth_date = timezone.now() - relativedelta(years=int(age))
            participant.birthday = datetime.combine(birth_date, time.min, tzinfo=pytz.timezone('Europe/Berlin'))
            participant.save()

        for i, message in enumerate(StringAttribute.objects.all()):
            message.string_field = f'Test String Attribute {i}'
            message.save()

        for i, message in enumerate(Message.objects.all()):
            message.supervisor = User.objects.get(id=1)
            message.message_body = f'Test Message {i}'
            message.internal_comment = ''
            message.created_by_email = None
            message.save()

        for i, workshop in enumerate(Workshop.objects.all()):
            workshop.free_text = f'Workshop Text {i}'
            workshop.supervisor = User.objects.get(id=1)
            workshop.save()

        for i, event in enumerate(Event.objects.all()):
            event.invitation_code_single = 'AAAA'
            event.invitation_code_group = 'AAAA'
            event.invitation_code = 'AAAA'
            event.keycloak_path = Group.objects.get(id=1)
            event.keycloak_admin_path = Group.objects.get(id=1)
            event.email_set = None
            event.save()
            event.responsible_persons.set(User.objects.filter(id=1))
