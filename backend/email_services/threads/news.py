import html

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.db.models import QuerySet
from django.template.context import make_context
from rest_framework.generics import get_object_or_404

from backend import settings
from email_services.choices import EmailType
from email_services.threads.helper import get_email, get_headers, get_scout_organisation_text, \
    get_event_pronoun
from event import models as event_models

url = getattr(settings, 'FRONT_URL', '')


@shared_task
def news_mail(evend_id: str, data: dict, email_type: EmailType):
    if not data['body']:
        return

    event: event_models.Event = get_object_or_404(event_models.Event, id=evend_id)
    technical_name = event.technical_name or 'info'
    sender = f'{event.name} <{technical_name}@{getattr(settings, "EMAIL_HOST_USER")}>'
    if data['subject']:
        subject = data['subject']
    else:
        subject = f'Neuigkeiten von: {event.name}'

    if data['header']:
        header = data['header']
    else:
        header = f'Neuigkeiten von: {event.name}'

    template_html, template_plain = get_email(email_type, event)

    event_name = html.escape(event.name)
    event_pronoun = get_event_pronoun(event_name)

    confirmed: bool = data.get('send_confirmed', True)
    unconfirmed: bool = data.get('send_unconfirmed', True)

    registrations: QuerySet[event_models.Registration] = event_models.Registration.objects.none()
    all_registrations = event.registration_set.all()

    if confirmed:
        confirmed_registrations = all_registrations.filter(is_confirmed=True)
        registrations = registrations | confirmed_registrations

    if unconfirmed:
        unconfirmed_registrations = all_registrations.filter(is_confirmed=False)
        registrations = registrations | unconfirmed_registrations

    for registration in registrations.all():
        scout_organisation = get_scout_organisation_text(registration)

        for person in registration.responsible_persons.all():
            if person.email is None or len(person.email) == 0:
                continue

            receiver = [person.email, ]

            data = {
                'responsible_persons': html.escape(person.userextended.scout_name) or '',
                'unsubscribe': person.userextended.id,
                'scout_organisation': scout_organisation,
                'event_name': event_name,
                'event_pronoun': event_pronoun,
                'custom_text': data['body'],
                'header': header
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
