import string

from openpyxl import load_workbook, Workbook
from openpyxl.styles import Alignment, Font
from openpyxl.styles.borders import Border, Side

from event import models as event_models
from event.file_generator.generators import helper
from event.file_generator.generators.abstract_generator import AbstractGenerator
from event.file_generator.generators.helper import get_participants_by_event
from event.file_generator.models import FileTemplate


class KjrGenerator(AbstractGenerator):

    def generate(self) -> Workbook:
        event: event_models.Event = self.generated_file.event

        file: FileTemplate = self.generated_file.template
        wb: Workbook = load_workbook(file.file)

        original = wb.active

        original['G1'] = event.name
        original['U1'] = helper.get_event_date(event)
        participants = get_participants_by_event(event)

        thin_border = Border(left=Side(style='thin'),
                             right=Side(style='thin'),
                             top=Side(style='thin'),
                             bottom=Side(style='thin'))
        alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        font_style = Font(size="11", name='Calibri')
        font_style_index = Font(size="11", name='Calibri', bold=True)

        participant: event_models.RegistrationParticipant

        for index, participant in enumerate(participants.all()):
            original[f'C{index + 5}'] = index
            original[f'C{index + 5}'].font = font_style_index
            original[f'C{index + 5}'].border = thin_border
            original[f'C{index + 5}'].alignment = alignment

            original[f'D{index + 5}'] = helper.get_participant_full_name(participant)
            original[f'E{index + 5}'] = helper.get_participant_age(event, participant)
            original[f'F{index + 5}'] = helper.get_participant_adress(participant)

            days: int = int(helper.get_participant_days(event, participant))
            for letter in string.ascii_uppercase[6: 6 + days]:
                original[f'{letter}{index + 5}'] = '/'

            for letter in string.ascii_uppercase[3: 21]:
                original[f'{letter}{index + 5}'].border = thin_border
                original[f'{letter}{index + 5}'].alignment = alignment
                original[f'{letter}{index + 5}'].font = font_style

        print(wb)
        return wb
