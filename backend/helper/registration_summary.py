import datetime

from django.utils.formats import date_format

from .email import send_responsible_person_mail, send_registration_summary, send_registration_reminder, send_matching
from basic.serializers import RegistrationSummarySerializer
from basic.models import Registration, RegistrationMatching, ScoutHierarchy, EventLocation
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict


def registration_responsible_person(data):
    send_responsible_person_mail(data)


def get_verband_name(parent_one):
    if (parent_one.level.id == 3):
        return 'BdP' if parent_one.id == 1 else 'DPV'
    else:
        partent_two = ScoutHierarchy.objects.filter(id=parent_one.parent.id).first()
        return 'BdP' if partent_two.id == 1 else 'DPV'


def create_registration_summary(data):
    RegistrationSerializer = RegistrationSummarySerializer()
    registration = get_object_or_404(Registration, pk=data['id'])
    total_participants = RegistrationSerializer.get_total_participants(obj=registration)
    total_fee = RegistrationSerializer.get_total_fee(obj=registration)

    for person in registration.responsible_persons.all():
        result = {
            'responsible_person': person.userextended.scout_name if person.userextended.scout_name is not None else person.username,
            'end_date': date_format(registration.event.registration_deadline),
            'scout_organisation': registration.scout_organisation,
            'event': registration.event.name,
            'event_id': registration.event.id,
            'email_id': registration.event.email_id,
            'responsible_persons': ', '.join(
                registration.responsible_persons.all().values_list('userextended__scout_name', flat=True)),
            'total_participants': total_participants,
            'total_fee': total_fee,
            'email': person.username
        }
        send_registration_summary(result)


def create_reminder_registration(registration):
    RegistrationSerializer = RegistrationSummarySerializer()
    total_participants = RegistrationSerializer.get_total_participants(obj=registration)
    total_volunteers = RegistrationSerializer.get_total_volunteers(obj=registration)

    for person in registration.responsible_persons.all():
        result = {
            'responsible_person': person.userextended.scout_name if person.userextended.scout_name is not None else person.username,
            'end_date': date_format(registration.event.registration_deadline),
            'scout_organisation': registration.scout_organisation,
            'event': registration.event.name,
            'event_id': registration.event.id,
            'email_id': registration.event.email_id,
            'responsible_persons': ', '.join(
                registration.responsible_persons.all().values_list('userextended__scout_name', flat=True)),
            'total_participants': total_participants,
            'total_volunteers': total_volunteers,
            'email': person.username,
            'confirmed': registration.is_confirmed
        }
        send_registration_reminder(result)


def create_matching_mail(match: RegistrationMatching, registration: Registration, matching_recipient):
    RegistrationSerializer = RegistrationSummarySerializer()
    total_participants = RegistrationSerializer.get_total_participants(obj=registration)
    total_volunteers = RegistrationSerializer.get_total_volunteers(obj=registration)
    total_groupleader = RegistrationSerializer.get_total_groupleader(obj=registration)
    total_leader = RegistrationSerializer.get_total_leader(obj=registration)
    total_costs = RegistrationSerializer.get_total_fee(obj=registration)

    if match:
        other_registrations = match.registrations.exclude(id=registration.id)
        if len(other_registrations) > 1:
            text_matching = "Eure Partnerstämme sind"
        else:
            text_matching = "Eure Partnerstamm ist der"

        for counter, other_registration in enumerate(other_registrations):
            if counter > 0:
                text_matching += " und"
            verband = get_verband_name(other_registration.scout_organisation)
            text_matching += f" {other_registration.scout_organisation.name} aus dem {verband}"
            resp_person = other_registration.responsible_persons.first()
            if resp_person is not None:
                text_matching += f", Kontakt {resp_person.userextended.scout_name}, {resp_person.username}"
        text_matching += "."

        location = match.event_location.city
        if match.sleeping_location.location_type is not None and 'Zelt' in match.sleeping_location.location_type.name:
            sleeping_location = f"auf dem Lagerplatz {match.sleeping_location.name}, "
        elif match.sleeping_location.location_type is not None and 'Heim' in match.sleeping_location.location_type.name:
            sleeping_location = f"im Heim {match.sleeping_location.name}, "
        else:
            sleeping_location = f"im {match.sleeping_location.name}, "
        sleeping_location += f"{match.sleeping_location.address} {match.sleeping_location.zip_code.zip_code} " \
                             f"{match.sleeping_location.zip_code.city} schlafen"

        if registration.eventlocation_set.count() > 0:
            location_registration: EventLocation = EventLocation.objects.filter(registration=registration)
            if 'Heim' in location_registration.first().location_type.name:
                type_name = 'Heim'
            else:
                type_name = "Zeltplatz"
            if RegistrationMatching.objects.filter(event=registration.event,
                                                   sleeping_location__in=location_registration).exists():
                text_location = f"Wir würden gern auf euer {type_name} " \
                                f"zurückgreifen. Bitte haltet dieses für das Wochenende frei."

            else:
                text_location = f"Vielen Dank für das Angebot, dass wir euer {type_name} " \
                                f"für die Veranstaltung nutzen könnten. Wir werden dieses aber nicht benötigen."
        else:
            text_location = ""

        if total_volunteers > 0:
            text_helper = f'Ihr habt {total_volunteers} Helfende angemeldet. ' \
                          f'Bitte schickt uns eine Mail-Adresse und wenn möglich, Handynummer,' \
                          f' damit wir uns bei diesen gesondert melden können. Gebt bitte den Doodle-Link ' \
                          f'https://doodle.com/poll/q9x5b3c62rk5fyrm?utm_source=poll&utm_medium=link' \
                          f' für ein digitales Treffen weiter.'
        else:
            text_helper = f'Ihr habt keine Helfenden angemeldet. ' \
                          f'Ist es möglich, dass die Stammesleitung eine Helfenden-Aufgabe in der Stadt übernimmt? ' \
                          f'Das bedeutet, die Person ist mit vor Ort, kann aber nicht als TN am Spiel teilnehmen. ' \
                          f'Wenn das möglich ist, dann bitte auch eine Mailadresse und wenn möglich Handynummer an uns' \
                          f', sowie den Doodle-Link ' \
                          f'https://doodle.com/poll/q9x5b3c62rk5fyrm?utm_source=poll&utm_medium=link weitergeben.'

        single_plural_scouthierachy = "eurem Partnerstamm" if other_registrations == 1 else "eurem Partnerstämmen"
        text_scouthierachies = ""
        for reg in other_registrations:
            text_scouthierachies += f'{reg.scout_organisation.name}:\n{reg.free_text}\n'

        final_date = date_format(datetime.datetime.now() + datetime.timedelta(days=7))

        for person in registration.responsible_persons.all():
            scout = registration.scout_organisation.name
            result = {
                'total_participants': total_participants,
                'total_volunteers': total_volunteers,
                'scout_organisation': str(scout),
                'total_groupleader': total_groupleader,
                'total_leader': total_leader,
                'email_id': registration.event.email_id,
                'total_costs': total_costs,
                'text_matching': text_matching,
                'location': location,
                'email': person.username,
                'sleeping_location': sleeping_location,
                'text_location': text_location,
                'final_date': final_date,
                'text_helper': text_helper,
                'single_plural_scouthierachy': single_plural_scouthierachy,
                'text_scouthierachies': text_scouthierachies,
                'recipient_matched': matching_recipient == 'matched'
            }
            send_matching(result)
