from django.db.models import QuerySet
from openpyxl import load_workbook, Workbook

from event import models as event_models
from event.file_generator.generators import helper
from event.file_generator.generators.abstract_generator import AbstractGenerator
from event.file_generator.models import FileTemplate


class KjpGeneratorComplex(AbstractGenerator):

    def generate(self) -> Workbook:
        event: event_models.Event = self.generated_file.event
        registrations: QuerySet[event_models.Registration] = helper.get_registrations(event)

        file: FileTemplate = self.generated_file.template
        wb: Workbook = load_workbook(file.file)
        original = wb.get_sheet_by_name('ListeVorlage')

        sheets_count = 0
        participants_count = 0
        registration: event_models.Registration
        sheets = []
        for registration in registrations:
            participants = registration.registrationparticipant_set.all().order_by('last_name')
            participant_count = participants.count()
            registration_index: int
            chunked_registration_indices: int
            for registration_index, chunked_registration_indices in enumerate(range(0, participant_count, 10)):
                registration_chunk = participants[chunked_registration_indices:chunked_registration_indices + 10]
                sheet = wb.copy_worksheet(original)
                sheets_count += 1
                sheet.title = f'{registration.scout_organisation.name}_{registration_index + 1}'
                sheets.append(sheet)

                sheet['T11'] = event.name
                sheet['AH11'] = helper.get_event_location(event)
                sheet['AQ11'] = helper.get_event_date(event)
                sheet['AX11'] = helper.get_event_days(event)

                participant: event_models.RegistrationParticipant
                for participant_index, participant in enumerate(registration_chunk):
                    cell = participant_index + 19
                    participants_count += 1
                    sheet[f'A{cell}'] = participants_count
                    sheet[f'C{cell}'] = f'{helper.get_participant_full_name(participant)}' \
                                        f'\n{helper.get_participant_adress(participant)}'
                    sheet[f'T{cell}'] = helper.get_participant_gender(participant)
                    sheet[f'V{cell}'] = helper.get_participant_state(participant)
                    sheet[f'Z{cell}'] = helper.get_particpant_below_27(event, participant)
                    sheet[f'BA{cell}'] = helper.get_participant_days(event, participant)

        wb.remove(original)

        for index, sheet in enumerate(sheets):
            sheet['AZ3'] = index
            sheet['BB3'] = sheets_count

        return wb
