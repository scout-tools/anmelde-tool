import html
import threading

from django.core.mail import EmailMultiAlternatives
from django.template.context import make_context
from rest_framework.generics import get_object_or_404

from backend import settings
from email_services.choices import EmailType
from email_services.threads.helper import get_email, get_headers, get_booking_options
from event import models as event_models
from event.summary.serializers import RegistrationCashSummarySerializer

url = getattr(settings, 'FRONT_URL', '')


class EmailThreadPaymentReminder(threading.Thread):
    def __init__(self, evend_id: str, email_type: EmailType):
        super().__init__()
        self.evend_id: str = evend_id
        self.email_type: EmailType = email_type

    def run(self) -> None:
        event: event_models.Event = get_object_or_404(event_models.Event, id=self.evend_id)

        technical_name = event.technical_name or 'info'
        sender = f'{event.name} <{technical_name}@{getattr(settings, "EMAIL_HOST_USER")}>'
        subject = f'Zahlungserinnerung für: {event.name}'

        template_html, template_plain = get_email(self.email_type, event)

        for registration in event.registration_set.all():
            serializer = RegistrationCashSummarySerializer(registration)

            if serializer.data['payement']['open'] <= 0:
                continue

            for person in registration.responsible_persons.all():
                if person.email is None or len(person.email) == 0:
                    continue

                receiver = [person.email, ]
                booking_options = get_booking_options(serializer.data['booking_options'])
                data = {
                    'responsible_persons': html.escape(person.userextended.scout_name) or '',
                    'unsubscribe': person.userextended.id,
                    'participant_count': serializer.data['participant_count'],
                    'booking_options': booking_options,
                    'sum': serializer.data['payement']['price'],
                    'received_sum': serializer.data['payement']['paid'],
                    'open_sum': serializer.data['payement']['open'],
                    'payment_id': serializer.data['ref_id']
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
