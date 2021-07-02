import datetime
from django.utils.formats import date_format
from basic.models import Registration, RegistrationMatching, EventLocation
from basic.serializers import RegistrationSummarySerializer
from .email import send_matching


def get_verband_name(parent_one):
    if parent_one.level.id == 3:
        return 'BdP' if parent_one.id == 1 else 'DPV'
    else:
        return get_verband_name(parent_one.parent)


def create_matching_mail(match: RegistrationMatching, registration: Registration, matching_recipient):
    RegistrationSerializer = RegistrationSummarySerializer()
    total_participants = RegistrationSerializer.get_total_participants(obj=registration)
    total_volunteers = RegistrationSerializer.get_total_volunteers(obj=registration)
    total_groupleader = RegistrationSerializer.get_total_groupleader(obj=registration)
    total_leader = RegistrationSerializer.get_total_leader(obj=registration)
    total_costs = RegistrationSerializer.get_total_fee(obj=registration)
    doodle_link = 'https://doodle.com/poll/q9x5b3c62rk5fyrm?utm_source=poll&utm_medium=link'
    if match:
        other_registrations = match.registrations.exclude(id=registration.id)
        text_matching = ""
        if len(other_registrations) > 0:
            text_matching += "<li>Das wichtigste zuerst: "

            if len(other_registrations) > 1:
                text_matching += "Eure Partnerstämme sind"
            else:
                text_matching += "Eure Partnerstamm ist der"

            for counter, other_registration in enumerate(other_registrations):
                if counter > 0:
                    text_matching += " und"
                verband = get_verband_name(other_registration.scout_organisation)
                text_matching += f" {other_registration.scout_organisation.name} aus dem {verband}"
                resp_person = other_registration.responsible_persons.first()
                if resp_person is not None:
                    text_matching += f", Kontakt {resp_person.userextended.scout_name}, " \
                                     f"<a href='mailto:{resp_person.username}' style='color:#ffffff'>{resp_person.username}</a>"
            text_matching += ".</li>"

        sleeping_location = ""
        if match.event_location is not None:
            sleeping_location += f"<li> Ihr werden das Spiel in {match.event_location.city} spielen"

        if match.sleeping_location is not None:
            sleeping_location += " und dort voraussichtlich "

            if match.sleeping_location.location_type is not None and 'Zelt' in match.sleeping_location.location_type.name:
                sleeping_location += f"auf dem Lagerplatz {match.sleeping_location.name}"
            elif match.sleeping_location.location_type is not None and 'Heim' in match.sleeping_location.location_type.name:
                sleeping_location += f"im Heim {match.sleeping_location.name}"
            else:
                sleeping_location = f"im {match.sleeping_location.name}"
            if match.sleeping_location.zip_code is not None:
                sleeping_location += f", {match.sleeping_location.address}," \
                                     f" {match.sleeping_location.zip_code.zip_code}," \
                                     f" {match.sleeping_location.zip_code.city}"

            sleeping_location += " schlafen.</li>"
        else:
            if match.event_location is not None:
                sleeping_location += ". </li>"
            sleeping_location += "<li>Wir klären grad noch die letzten Details zu den Schlafplätzen und melden uns, " \
                                 "sobald diese feststehen. </li>"
        if len(other_registrations) == 0:
            sleeping_location += "<li>Genauso verhält es sich mit eurem Partnerstamm. " \
                                 "Sobald wir diese zugeteilt haben, melden wir uns. </li>"

        if registration.eventlocation_set.count() > 0:
            location_registration: EventLocation = EventLocation.objects.filter(registration=registration)
            if 'Heim' in location_registration.first().location_type.name:
                type_name = 'Heim'
            else:
                type_name = "Zeltplatz"
            if RegistrationMatching.objects.filter(event=registration.event,
                                                   sleeping_location__in=location_registration).exists():
                text_location = f"<li>Wir würden gern auf euer {type_name} " \
                                f"zurückgreifen. Bitte haltet dieses für das Wochenende frei.</li>"

            else:
                text_location = f"<li>Vielen Dank für das Angebot, dass wir euer {type_name} " \
                                f"für die Veranstaltung nutzen könnten. Wir werden dieses aber nicht benötigen.</li>"
        else:
            text_location = ""

        if total_volunteers > 0:
            text_helper = f'Ihr habt {total_volunteers} Helfende angemeldet. ' \
                          f'Bitte schickt uns eine Mail-Adresse und wenn möglich, Handynummer,' \
                          f' damit wir uns bei diesen gesondert melden können. Gebt bitte den ' \
                          f'<a href="{doodle_link}" style="color:#ffffff">Doodle-Link</a>' \
                          f' für ein digitales Treffen weiter.'
        else:
            text_helper = f'Ihr habt keine Helfenden angemeldet. ' \
                          f'Ist es möglich, dass die Stammesleitung eine Helfenden-Aufgabe in der Stadt übernimmt? ' \
                          f'Das bedeutet, die Person ist mit vor Ort, kann aber nicht als TN am Spiel teilnehmen. ' \
                          f'Wenn das möglich ist, dann bitte auch eine Mailadresse und wenn möglich Handynummer an uns' \
                          f', sowie den <a href="{doodle_link}" style="color:#ffffff">Doodle-Link</a>'

        single_plural_scouthierachy = "eurem Partnerstamm" if other_registrations == 1 else "euren Partnerstämmen"
        text_scouthierachies = ""
        for reg in other_registrations:

            if not reg.free_text:
                reg.free_text = "Der Stamm hat leider keine Nachricht hinterlassen."
            text_scouthierachies += f'<p>{reg.scout_organisation.name}:<br>{reg.free_text}</p>'

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
