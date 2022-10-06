from dateutil.relativedelta import relativedelta
from django.db.models import QuerySet

from event import models as event_models


def get_registrations(event: event_models.Event) -> QuerySet[event_models.Registration]:
    return event_models.Registration.objects.filter(event=event, is_confirmed=True)


def get_event_location(event: event_models.Event) -> str:
    if event.location:
        return f'{event.location.address}, {event.location.zip_code.zip_code} {event.location.zip_code.city}'
    else:
        return ''


def get_event_date(event: event_models.Event) -> str:
    if event.start_date and event.end_date:
        return f'{event.start_date.date().strftime("%d.%m.%Y")} - {event.end_date.date().strftime("%d.%m.%Y")}'
    else:
        return ''


def get_event_days(event: event_models.Event) -> str:
    if event.end_date and event.start_date:
        return str((event.end_date.date() - event.start_date.date()).days + 1)
    else:
        return ''


def get_event_short_description(event: event_models.Event) -> str:
    if event.short_description:
        return event.short_description
    else:
        return ''


def get_participant_age(event: event_models.Event, participant: event_models.RegistrationParticipant) -> int:
    if participant.birthday:
        return relativedelta(event.start_date.date(), participant.birthday.date()).years
    else:
        return 0


def get_participant_first_name(participant: event_models.RegistrationParticipant) -> str:
    if participant.first_name:
        return participant.first_name
    else:
        return ''


def get_participant_last_name(participant: event_models.RegistrationParticipant) -> str:
    if participant.last_name:
        return participant.last_name
    else:
        return ''


def get_participant_scout_name(participant: event_models.RegistrationParticipant) -> str:
    if participant.scout_name:
        return participant.scout_name
    else:
        return ''


def get_participant_full_name(participant: event_models.RegistrationParticipant) -> str:
    full_name = f'{get_participant_first_name(participant)} {get_participant_last_name(participant)}'
    return full_name.strip()


def get_participant_street(participant: event_models.RegistrationParticipant) -> str:
    if participant.street:
        return participant.street
    else:
        return ''


def get_participant_zip_city(participant: event_models.RegistrationParticipant) -> str:
    if participant.zip_code:
        return f'{participant.zip_code.zip_code} {participant.zip_code.city}'
    else:
        return ''


def get_participant_adress(participant: event_models.RegistrationParticipant) -> str:
    street = get_participant_street(participant)
    zip_city = get_participant_zip_city(participant)
    full_adress = ''
    if street:
        full_adress += f'{participant.street}'
    if zip_city:
        if street:
            full_adress += ', '
        full_adress += f'{participant.zip_code.zip_code} {participant.zip_code.city}'

    return full_adress


def get_participant_state(participant: event_models.RegistrationParticipant) -> str:
    states = {
        'BW': 'Baden-Württemberg',
        'BY': 'Bayern',
        'BE': 'Berlin',
        'BB': 'Brandenburg',
        'HB': 'Bremen',
        'HH': 'Hamburg',
        'HE': 'Hessen',
        'MV': 'Mecklenburg-Vorpommern',
        'NI': 'Niedersachsen',
        'NW': 'Nordrhein-Westfalen',
        'RP': 'Rheinland-Pfalz',
        'SL': 'Saarland',
        'SN': 'Sachsen',
        'ST': 'Sachsen-Anhalt',
        'SH': 'Schleswig-Holstein',
        'TH': 'Thüringen'
    }
    if participant.zip_code and participant.zip_code.state:
        return states.get(participant.zip_code.state, '')
    else:
        return ''


def get_participant_gender(participant: event_models.RegistrationParticipant) -> str:
    if participant.gender:
        if participant.gender == 'N':
            return '/'
        elif participant.gender == 'F':
            return 'W'
        else:
            return participant.gender
    else:
        return ''


def get_participant_days(event: event_models.Event, participant: event_models.RegistrationParticipant) -> str:
    if participant.booking_option and participant.booking_option.start_date and participant.booking_option.end_date:
        return str((participant.booking_option.end_date.date() - participant.booking_option.start_date.date()).days + 1)
    elif event.start_date and event.end_date:
        return str((event.end_date.date() - event.start_date.date()).days + 1)
    else:
        return ''


def get_particpant_below_27(event: event_models.Event, participant: event_models.RegistrationParticipant) -> str:
    if participant.birthday:
        return 'Ja' if get_participant_age(event, participant) < 27 else 'Nein'
    else:
        return ''


def get_participant_mobile_numer(participant: event_models.RegistrationParticipant) -> str:
    if participant.phone_number:
        return participant.phone_number
    else:
        return ''


def get_participant_email(participant: event_models.RegistrationParticipant) -> str:
    if participant.email:
        return participant.email
    else:
        return ''


def get_registration_scout_organistation_name(registration: event_models.Registration) -> str:
    if registration.scout_organisation:
        return registration.scout_organisation.name
    else:
        return ''


def get_participant_registration_scout_organisation_name(participant: event_models.RegistrationParticipant) -> str:
    if participant.registration:
        return get_registration_scout_organistation_name(participant.registration)
    else:
        return ''


def get_participants_by_event(event: event_models.Event) -> QuerySet[event_models.RegistrationParticipant]:
    registrations = get_registrations(event).values_list('id', flat=True)
    return event_models.RegistrationParticipant.objects.filter(registration__in=registrations) \
        .order_by('registration__scout_organisation__name', 'last_name')


def get_booking_options_name(event: event_models.Event):
    return list(event.bookingoption_set.exclude(name__contains='Tagesgast').values_list('name', flat=True))


def get_formatted_booking_option(registration: event_models.Registration, booking_options_name: str):
    if booking_options_name != 'Tagesgast':
        result = registration.registrationparticipant_set.filter(booking_option__name=booking_options_name).count()
    else:
        result = registration.registrationparticipant_set \
            .filter(booking_option__name__contains=booking_options_name).count()
    return result or 0


def get_participants_by_registration(registration=None) -> QuerySet[event_models.RegistrationParticipant]:
    return event_models.RegistrationParticipant.objects.filter(registration=registration).order_by('last_name')
