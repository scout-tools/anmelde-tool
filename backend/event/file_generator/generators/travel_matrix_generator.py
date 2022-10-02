from django.db.models import QuerySet, Count
from openpyxl import load_workbook, Workbook
from openpyxl.worksheet.worksheet import Worksheet

from basic.choices import TravelType, TravelSlots
from event import models as event_models
from event.file_generator.generators import helper
from event.file_generator.generators.abstract_generator import AbstractGenerator
from event.file_generator.models import FileTemplate


class TravelMatrixGenerator(AbstractGenerator):

    def generate(self) -> Workbook:
        event: event_models.Event = self.generated_file.event
        registrations: QuerySet[event_models.Registration] = helper.get_registrations(event)
        file: FileTemplate = self.generated_file.template
        wb: Workbook = load_workbook(file.file)

        original: Worksheet = wb.active

        participant_count = registrations.aggregate(count=Count('registrationparticipant'))['count'] or 0

        original['B1'] = f'{event.name} \n{helper.get_event_location(event)}'
        original['E1'] = helper.get_event_date(event)
        original['G1'] = participant_count

        travel_type_mapping = {
            'T': 3,
            'B': 4,
            'C': 5,
            'O': 6,
            'sum': 7
        }

        travel_time_mapping = {
            'B': 'B',
            'E': 'C',
            'N': 'D',
            'L': 'E',
            'SL': 'F',
            'O': 'G',
            'sum': 'H'
        }

        time_sum = {
            'B': 0,
            'E': 0,
            'N': 0,
            'L': 0,
            'SL': 0,
            'O': 0,
        }

        type_complete_sum = 0
        for travel_type in TravelType:
            type_filtered: QuerySet = registrations.filter(tags__travelattribute__type_field=travel_type)

            for travel_time in TravelSlots:
                time_filtered: QuerySet = type_filtered.filter(tags__travelattribute__time_field=travel_time)
                travel_sum: int = time_filtered.aggregate(count=Count('registrationparticipant'))['count'] or 0
                field = f'{travel_time_mapping[travel_time]}{travel_type_mapping[travel_type]}'
                original[field] = travel_sum

                time_sum[travel_time] += travel_sum

            field_type_sum = f'{travel_time_mapping["sum"]}{travel_type_mapping[travel_type]}'
            type_sum = type_filtered.aggregate(count=Count('registrationparticipant'))['count'] or 0
            original[field_type_sum] = type_sum
            type_complete_sum += type_sum

        time_complete_sum = 0
        for travel_time in TravelSlots:
            field_time_sum = f'{travel_time_mapping[travel_time]}{travel_type_mapping["sum"]}'
            original[field_time_sum] = time_sum[travel_time]
            time_complete_sum += time_sum[travel_time]

        if time_complete_sum == type_complete_sum:
            final_sum = time_complete_sum
        else:
            final_sum = f'{time_complete_sum}/{type_complete_sum}'
        original['H7'] = final_sum

        return wb
