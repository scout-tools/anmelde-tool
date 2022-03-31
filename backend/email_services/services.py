from datetime import datetime
from django.core.mail import EmailMultiAlternatives
from django.db.models import Sum
from django.template import Context, Template
from django.template.context import make_context
import threading
from threading import Thread

from rest_framework.generics import get_object_or_404

from backend import settings
from event import models as event_models
from email_services import models as email_services_models
from .choices import EmailType

url = getattr(settings, 'FRONT_URL', '')
email_active = getattr(settings, 'SEND_MAIL', False)


def send_registration_created_mail(**kwargs):
    instance_id = kwargs.get('instance_id')
    if instance_id and email_active:
        EmailThreadRegistration(instance_id, EmailType.RegistrationCreated).start()


class EmailThreadRegistration(threading.Thread):
    def __init__(self, registration_id: str, email_type: EmailType):
        super().__init__()
        self.registration_id: str = registration_id
        self.email_type: EmailType = email_type

    def run(self) -> None:
        registration: event_models.Registration = get_object_or_404(event_models.Registration, id=self.registration_id)

        sender = f'{registration.event.name} <{registration.event.technical_name}@{getattr(settings, "EMAIL_HOST_USER")}>'
        subject = f'Registrierungsbestätigung für: {registration.event.name}'

        email_type_mapping = {
            EmailType.RegistrationCreated: registration.event.email_set.registration_created,
            EmailType.RegistrationUpdated: registration.event.email_set.registration_updated,
            EmailType.RegistrationAccepted: registration.event.email_set.registration_accepted,
            EmailType.RegistrationReminder: registration.event.email_set.registration_reminder
        }

        files: email_services_models.Email = email_type_mapping.get(self.email_type,
                                                                    registration.event.email_set.registration_created)
        html_body_template = files.html
        plain_body_template = files.plain

        template_html = Template(html_body_template)
        template_plain = Template(plain_body_template)

        count = registration.registrationparticipant_set.count() or 0
        participant_sum = registration.registrationparticipant_set \
                              .aggregate(sum=Sum('booking_option__price'))['sum'] or 0
        if count > 0:
            list_participants = '<ul>'
            for participant in registration.registrationparticipant_set.all():
                particpiant_entry = f'<li>{participant.first_name}, {participant.last_name}'
                if participant.scout_name:
                    particpiant_entry += f' ({participant.scout_name})'
                particpiant_entry += f': {participant.booking_option.name}, {participant.booking_option.price}&#8364;'
                particpiant_entry += '</li>'
                list_participants += particpiant_entry
            list_participants += '</ul>'
        else:
            list_participants = ''

        for person in registration.responsible_persons.all():
            receiver = [person.email, ]

            data = {
                'responsible_persons': person.userextended.scout_name or '',
                'unsubscribe': person.userextended.id,
                'participant_count': count,
                'sum': participant_sum,
                'list_participants': list_participants,
                'scout_organisation': registration.scout_organisation.name
            }

            headers = {
                'List-Unsubscribe': f'<mailto: {sender}?subject=unsubscribe>, <{url}/unsubscribe/{person.userextended.id}/>',
                'List-Unsubscribe-Post': 'List-Unsubscribe=One-Click'
            }

            html_rendered = template_html.render(make_context(data, autoescape=False))
            plain_rendered = template_plain.render(make_context(data, autoescape=False))

            email = EmailMultiAlternatives(subject=subject,
                                           body=plain_rendered,
                                           from_email=sender,
                                           to=receiver,
                                           headers=headers,
                                           reply_to=[sender, ])
            email.attach_alternative(html_rendered, "text/html")
            email.send(fail_silently=False)

            print(f'mail sent at {datetime.now()}')
