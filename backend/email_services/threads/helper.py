from django.db.models import Sum, F, Count, QuerySet
from django.template import Template
import html
from backend import settings
from email_services import models as email_services_models
from email_services.choices import EmailType
from event import models as event_models

url = getattr(settings, 'FRONT_URL', '')


def get_email(email_type: EmailType, event: event_models.Event) -> [Template, Template]:
    if event.email_set is None:
        return None, None
    email_type_mapping = {
        EmailType.RegistrationCreated: event.email_set.registration_created,
        EmailType.RegistrationUpdated: event.email_set.registration_updated,
        EmailType.RegistrationAccepted: event.email_set.registration_accepted,
        EmailType.RegistrationReminder: event.email_set.registration_reminder,
        EmailType.PaymentReminder: event.email_set.payment_reminder,
        EmailType.StandardEmail: event.email_set.custom_mail
    }
    files: email_services_models.Email = email_type_mapping.get(email_type, event.email_set.registration_created)

    html_body_template = files.html
    plain_body_template = files.plain
    template_html = Template(html_body_template)
    template_plain = Template(plain_body_template)
    return template_html, template_plain


def get_headers(person, sender):
    headers = {
        'List-Unsubscribe': f'<mailto: {sender}?subject=unsubscribe>, <{url}/unsubscribe/{person.userextended.id}/>',
        'List-Unsubscribe-Post': 'List-Unsubscribe=One-Click'
    }
    return headers


def get_event_pronoun(event_name: str) -> str:
    name_lower = event_name.lower()
    if any(tmp in name_lower for tmp in ['lager', 'busife']):
        return 'das'
    if any(tmp in name_lower for tmp in ['aktion', 'fahrt']):
        return 'die'
    else:
        return 'das'


def get_html_participant_list(registration: event_models.Registration) -> str:
    list_participants = '<ul>'
    for participant in registration.registrationparticipant_set.all():
        particpiant_entry = f'<li>{participant.first_name}, {participant.last_name}'
        if participant.scout_name:
            particpiant_entry += f' ({participant.scout_name})'
        particpiant_entry += f': {participant.booking_option.name}, {participant.booking_option.price}&#8364;'
        particpiant_entry += '</li>'
        list_participants += particpiant_entry
    list_participants += '</ul>'
    return list_participants


def get_participant_count(registration: event_models.Registration) -> [int, int]:
    count = registration.registrationparticipant_set.count() or 0
    participant_sum = registration.registrationparticipant_set \
                          .aggregate(sum=Sum('booking_option__price'))['sum'] or 0
    return count, participant_sum


def get_booking_options(booking_options: QuerySet) -> str:
    result: str = ''
    for index, option in enumerate(booking_options.all()):
        if index > 0:
            result += ', '
        result += f'{option["sum"]} {option["booking_options"]}'
    return result


def get_scout_organisation_text(registration):
    scout_orga_unit_name = 'Stamm' if registration.scout_organisation.level.id == 5 else ''
    if not registration.single:
        scout_organisation = f'{scout_orga_unit_name} {html.escape(registration.scout_organisation.name)}'
    else:
        scout_organisation = f'Einzelpersonen aus dem {scout_orga_unit_name} {html.escape(registration.scout_organisation.name)}'
    return scout_organisation
