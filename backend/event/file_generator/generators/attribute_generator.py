import string

from django.db.models import QuerySet, Count, Sum
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Alignment, Font
from openpyxl.worksheet.worksheet import Worksheet

from basic import models as basic_models
from event import models as event_models
from event.file_generator.generators import helper
from event.file_generator.generators.abstract_generator import AbstractGenerator
from event.file_generator.generators.helper import get_participants_by_registration
from event.file_generator.models import FileTemplate


class AttributeGenerator(AbstractGenerator):

    def generate(self) -> Workbook:
        event: event_models.Event = self.generated_file.event
        registrations: QuerySet[event_models.Registration] = helper.get_registrations(event)
        file: FileTemplate = self.generated_file.template
        wb: Workbook = load_workbook(file.file)

        original: Worksheet = wb.active
        original.sheet_format.defaultRowHeight = 25.0
        original.set_printer_settings(paper_size=original.PAPERSIZE_A4, orientation='landscape')

        participant_count = registrations.aggregate(count=Count('registrationparticipant'))['count'] or 0
        table = original.tables['Teilnehmer']
        table.ref = f'A2:G{registrations.count() + 2}'

        original['C1'] = f'{event.name} \n{helper.get_event_location(event)}'
        original['E1'] = helper.get_event_date(event)
        original['G1'] = participant_count

        alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        font_style = Font(size="10", name='Calibri')

        index: int = 3
        registration: event_models.Registration
        for registration in registrations.all().order_by('scout_organisation__name'):
            travel_tag: basic_models.TravelAttribute = registration.tags.instance_of(
                basic_models.TravelAttribute).first()
            tent_small_tag: basic_models.IntegerAttribute = registration.tags.filter(template_id=17).first()
            tent_large_tag: basic_models.IntegerAttribute = registration.tags.filter(template_id=19).first()

            all_participants = get_participants_by_registration(registration)
            original[f'A{index}'] = index - 2
            original[f'B{index}'] = helper.get_registration_scout_organistation_name(registration)
            original[f'C{index}'] = all_participants.count()

            if travel_tag:
                original[f'D{index}'] = travel_tag.get_type_field_display()
                original[f'E{index}'] = travel_tag.get_time_field_display()

            if tent_small_tag:
                original[f'F{index}'] = tent_small_tag.integer_field

            if tent_large_tag:
                original[f'G{index}'] = tent_large_tag.integer_field

            original.row_dimensions[index].height = 25
            for letter in string.ascii_uppercase[:7]:
                original[f'{letter}{index}'].alignment = alignment
                original[f'{letter}{index}'].font = font_style

            index += 1

        mapper_ids = registrations.values_list('tags', flat=True)
        attributes = basic_models.AbstractAttribute.objects.filter(id__in=mapper_ids)

        count_tent_small: int = \
            attributes.filter(template_id=17).aggregate(count=Sum('integerattribute__integer_field'))['count'] or 0
        count_tent_large: int = \
            attributes.filter(template_id=19).aggregate(count=Sum('integerattribute__integer_field'))['count'] or 0

        original[f'C{index}'] = participant_count
        original[f'F{index}'] = count_tent_small
        original[f'G{index}'] = count_tent_large

        original.row_dimensions[index].height = 25
        for letter in string.ascii_uppercase[:7]:
            original[f'{letter}{index}'].alignment = alignment
            original[f'{letter}{index}'].font = font_style

        return wb
