from datetime import datetime
from django.core.mail import EmailMultiAlternatives
from django.db.models import Sum
from django.template import Context, Template
from django.template.context import make_context
from eb_sqs_worker.decorators import task
from rest_framework.generics import get_object_or_404

from backend import settings
from event import models as event_models
from email_services import models as email_services_models

url = getattr(settings, 'FRONT_URL', '')


@task
def send_registration_created_mail(**kwargs):
    print('signal received')
    instance_id = kwargs.get('instance_id')
    if instance_id:
        instance: event_models.Registration = get_object_or_404(event_models.Registration, id=instance_id)
        sender = f'{instance.event.name} <{instance.event.technical_name}@{getattr(settings, "EMAIL_HOST_USER")}>'
        # sender = 'Anmelde-Tool <info@anmelde-tool.de>'
        subject = f'Deine Registrierung bei {instance.event.name}'

        files: email_services_models.Email = instance.event.email_set.registration_created
        html_body_template = files.html
        plain_body_template = files.plain

        template_html = Template(html_body_template)
        template_plain = Template(plain_body_template)

        count = instance.registrationparticipant_set.count()
        participant_sum = instance.registrationparticipant_set.aggregate(sum=Sum('booking_option__price'))['sum'] or 0

        for person in instance.responsible_persons.all():
            receiver = [person.email, ]

            data = {
                'responsible_persons': person.userextended.scout_name,
                'unsubscribe': person.userextended.id,
                'participant_count': count,
                'sum': participant_sum
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
    return True
