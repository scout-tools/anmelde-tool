from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.utils.formats import date_format
from openpyxl import load_workbook, Workbook

from basic.models import StringAttribute
from event import models as event_models
from event.file_generator.generators import helper
from event.file_generator.generators.abstract_generator import AbstractGenerator
from event.file_generator.models import FileTemplate
from event.summary.serializers import RegistrationCashSummarySerializer


class InvoiceGenerator(AbstractGenerator):

    def generate(self) -> Workbook:
        event: event_models.Event = self.generated_file.event
        registrations: QuerySet[event_models.Registration] = helper.get_registrations(event)
        file: FileTemplate = self.generated_file.template
        wb = load_workbook(file.file)
        original = wb.active
        booking_options: list[str] = get_booking_options_name(event)[:3]

        if len(booking_options) > 0:
            original['K1'] = booking_options[0]
        else:
            original['K1'] = 'Nicht belegt'

        if len(booking_options) > 1:
            original['L1'] = booking_options[1]
        else:
            original['L1'] = 'Nicht belegt'

        if len(booking_options) > 2:
            original['M1'] = booking_options[2]
        else:
            original['M1'] = 'Nicht belegt'

        index: int = 1
        registration: event_models.Registration
        for registration in registrations.all():
            serialized = RegistrationCashSummarySerializer(registration).data
            person_1: User = registration.responsible_persons.first()
            person_2: User = None
            if registration.responsible_persons.count() > 1:
                person_2 = registration.responsible_persons.all()[1]
            letter: StringAttribute = registration.tags.instance_of(StringAttribute).first()
            payment = serialized.get('payement', None)
            price = payment.get('price', 0) if payment else 0

            all_participants = get_participants_by_registration(registration)
            participant_list = [helper.get_participant_full_name(participant) for participant in all_participants.all()]

            original[f'A{index + 1}'] = index
            original[f'B{index + 1}'] = helper.get_registration_scout_organistation_name(registration)
            original[f'C{index + 1}'] = date_format(registration.created_at.date(), format='SHORT_DATE_FORMAT')
            original[f'D{index + 1}'] = date_format(registration.updated_at.date(), format='SHORT_DATE_FORMAT')
            original[f'E{index + 1}'] = person_1.first_name
            original[f'F{index + 1}'] = person_1.last_name
            original[f'G{index + 1}'] = person_1.email

            if person_2:
                original[f'H{index + 1}'] = person_2.first_name
                original[f'I{index + 1}'] = person_2.last_name
                original[f'J{index + 1}'] = person_2.email

            if len(booking_options) > 0:
                original[f'K{index + 1}'] = get_formatted_booking_option(registration, booking_options[0])
            if len(booking_options) > 1:
                original[f'L{index + 1}'] = get_formatted_booking_option(registration, booking_options[1])
            if len(booking_options) > 2:
                original[f'M{index + 1}'] = get_formatted_booking_option(registration, booking_options[2])
            original[f'N{index + 1}'] = get_formatted_booking_option(registration, 'Tagesgast')

            original[f'O{index + 1}'] = serialized.get('participant_count', 0)
            original[f'P{index + 1}'] = price
            original[f'Q{index + 1}'] = letter.string_field if letter else ''
            original[f'R{index + 1}'] = ',\n'.join(participant_list)
            original[f'S{index + 1}'] = f'{registration.event.name.replace(" ", "")[:10]}' \
                                        f'-{registration.scout_organisation.name.replace(" ", "")[:10]}' \
                                        f'-{str(registration.created_at.timestamp())[:10]}'
            index += 1

        return wb
