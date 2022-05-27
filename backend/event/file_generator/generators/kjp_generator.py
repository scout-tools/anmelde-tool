from django.db.models import QuerySet
from dateutil.relativedelta import relativedelta
from openpyxl import load_workbook, Workbook

from event.file_generator.generators.abstract_generator import AbstractGenerator
from event.file_generator.models import FileTemplate, GeneratedFiles
from event import models as event_models


class KjpGenerator(AbstractGenerator):

    def generate(self) -> Workbook:
        event: event_models.Event = self.get_event()
        participants = self.get_participants(event)
        file: FileTemplate = self.generated_file.template
        wb: Workbook = load_workbook(file.file)
        original = wb.get_sheet_by_name('L_1_DPBM')
        sheets = []

        for i in range(0, int(len(participants) / 10) + 1, 1):
            sheets.append(wb.copy_worksheet(original))
        wb.remove(original)

        for index_sheets, i in enumerate(range(0, len(participants), 10)):
            location = f'{event.location.address}, {event.location.zip_code.zip_code} {event.location.zip_code.city}'
            event_date = f'{event.start_date.date().strftime("%d.%m.%Y")} - {event.end_date.date().strftime("%d.%m.%Y")}'
            event_days = (event.end_date.date() - event.start_date.date()).days
            sheets[index_sheets].title = f'L_{index_sheets + 1}_{event.limited_registration_hierarchy.name}'
            sheets[index_sheets]['A9'] = event.name
            sheets[index_sheets]['T9'] = event.short_description
            sheets[index_sheets]['AH9'] = location
            sheets[index_sheets]['AP9'] = f'{event.start_date.date()} - {event.end_date.date()}'
            sheets[index_sheets]['AP9'] = event_date
            sheets[index_sheets]['AW9'] = event_days
            sheets[index_sheets]['AZ1'] = index_sheets + 1

            for index, chunk in enumerate(participants[i:i + 10]):
                cell = index * 3 + 17
                age = relativedelta(event.start_date.date(), chunk.birthday.date()).years
                full_name = f'{chunk.first_name} {chunk.last_name}'
                adress = f'{chunk.street}, {chunk.zip_code.zip_code} {chunk.zip_code.city}'
                gender = chunk.gender if chunk.gender != 'N' else '/'
                if chunk.booking_option and chunk.booking_option.start_date and chunk.booking_option.end_date:
                    participant_days = (
                            chunk.booking_option.end_date.date() - chunk.booking_option.start_date.date()).days
                else:
                    participant_days = event_days
                sheets[index_sheets][f'A{cell}'] = index_sheets * 10 + index + 1
                sheets[index_sheets][f'C{cell}'] = f'{full_name}\n{adress}'
                sheets[index_sheets][f'T{cell}'] = gender
                sheets[index_sheets][f'V{cell}'] = chunk.zip_code.state
                sheets[index_sheets][f'Z{cell}'] = 'Ja' if age < 27 else 'Nein'
                sheets[index_sheets][f'AQ{cell}'] = participant_days

        return wb

    def get_participants(self, event) -> QuerySet[event_models.RegistrationParticipant]:
        registrations = event_models.Registration.objects.filter(event=event, is_confirmed=True) \
            .values_list('id', flat=True)
        participants = event_models.RegistrationParticipant.objects.filter(registration__in=registrations) \
            .order_by('last_name')
        return participants

    def get_event(self) -> event_models.Event:
        return self.generated_file.event
