from django.db.models import QuerySet
from dateutil.relativedelta import relativedelta
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Alignment, Font
import string

from event.file_generator.generators.abstract_generator import AbstractGenerator
from event.file_generator.models import FileTemplate
from event import models as event_models


class ParticipantGenerator(AbstractGenerator):

    def generate(self) -> Workbook:
        event: event_models.Event = self.get_event()
        participants = self.get_participants(event)
        file: FileTemplate = self.generated_file.template
        wb: Workbook = load_workbook(file.file)
        original = wb.active
        original.sheet_format.defaultRowHeight = 25.0
        original.set_printer_settings(paper_size=original.PAPERSIZE_A4, orientation='landscape')

        table = original.tables['Teilnehmer']
        table.ref = f'A3:J{participants.count() + 3}'
        location = f'{event.location.address}, {event.location.zip_code.zip_code} {event.location.zip_code.city}'

        original['C1'] = f'{event.name}\n{location}'
        original['G1'] = f'{event.start_date.date().strftime("%d.%m.%Y")}' \
                         f' - {event.end_date.date().strftime("%d.%m.%Y")}'
        original['J1'] = participants.count()

        alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        font_style = Font(size="10", name='Calibri')

        participant: event_models.RegistrationParticipant
        for index, participant in enumerate(participants.all()):
            original[f'A{index + 4}'] = participant.first_name
            original[f'B{index + 4}'] = participant.last_name
            original[f'C{index + 4}'] = participant.scout_name
            original[f'D{index + 4}'] = relativedelta(event.start_date.date(), participant.birthday.date()).years
            original[f'E{index + 4}'] = participant.gender if participant.gender != 'N' else '/'
            original[f'F{index + 4}'] = participant.phone_number
            original[f'G{index + 4}'] = participant.email
            original[f'H{index + 4}'] = participant.registration.scout_organisation.name
            original[f'I{index + 4}'] = participant.street
            original[f'J{index + 4}'] = f'{participant.zip_code.zip_code} {participant.zip_code.city}'

            original.row_dimensions[index + 4].height = 25
            for letter in string.ascii_uppercase[:10]:
                original[f'{letter}{index + 4}'].alignment = alignment
                original[f'{letter}{index + 4}'].font = font_style

        return wb

    def get_participants(self, event) -> QuerySet[event_models.RegistrationParticipant]:
        registrations = event_models.Registration.objects.filter(event=event, is_confirmed=True) \
            .values_list('id', flat=True)
        participants = event_models.RegistrationParticipant.objects.filter(registration__in=registrations) \
            .order_by('registration__scout_organisation__name', 'last_name')
        return participants

    def get_event(self) -> event_models.Event:
        return self.generated_file.event
