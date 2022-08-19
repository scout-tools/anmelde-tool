import html
import threading

from django.core.mail import EmailMultiAlternatives
from django.template.context import make_context
from rest_framework.generics import get_object_or_404

from backend import settings
from email_services.choices import EmailType
from email_services.threads.helper import get_email, get_headers, get_event_pronoun, get_html_participant_list, \
    get_participant_count, get_scout_organisation_text
from event import models as event_models

url = getattr(settings, 'FRONT_URL', '')


class EmailThreadRegistration(threading.Thread):
    def __init__(self, registration_id: str, email_type: EmailType):
        super().__init__()
        self.registration_id: str = registration_id
        self.email_type: EmailType = email_type

    def run(self) -> None:
        registration: event_models.Registration = get_object_or_404(event_models.Registration, id=self.registration_id)
        event: event_models.Event = registration.event

        technical_name = event.technical_name or 'info'
        sender = f'{event.name} <{technical_name}@{getattr(settings, "EMAIL_HOST_USER")}>'
        subject = f'Registrierungsbestätigung für: {event.name}'

        template_html, template_plain = get_email(self.email_type, event)

        count, participant_sum = get_participant_count(registration)

        if count > 0:
            list_participants = get_html_participant_list(registration)
        else:
            list_participants = ''

        event_name = html.escape(event.name)
        event_pronoun = get_event_pronoun(event_name)

        scout_organisation = get_scout_organisation_text(registration)

        for person in registration.responsible_persons.all():
            receiver = [person.email, ]

            data = {
                'event_name': event_name,
                'event_pronoun': event_pronoun,
                'responsible_persons': html.escape(person.userextended.scout_name) or '',
                'unsubscribe': person.userextended.id,
                'participant_count': count,
                'sum': participant_sum,
                'list_participants': list_participants,
                'scout_organisation': scout_organisation
            }

            headers = get_headers(person, sender)

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
