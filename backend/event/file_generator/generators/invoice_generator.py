import os
import threading
import time
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import QuerySet
from dateutil.relativedelta import relativedelta
from openpyxl import load_workbook, Workbook
from django.core.files.base import File
from tempfile import NamedTemporaryFile
from backend import settings
from event.choices.choices import FileGenerationStatus, FileType, FileExtension
from event.file_generator.generators.abstract_generator import AbstractGenerator
from event.file_generator.models import FileTemplate, GeneratedFiles
from event import models as event_models
from django.contrib.auth.models import User
from django.db.models import Q
from event.summary.serializers import RegistrationCashSummarySerializer
from basic.models import StringAttribute


class InvoiceGenerator(AbstractGenerator):

    def generate(self) -> Workbook:
        event: event_models.Event = self.get_event()
        registrations: QuerySet[event_models.Registration] = self.get_registrations(event)
        file: FileTemplate = self.generated_file.template
        wb = load_workbook(file.file)
        original = wb.active

        index: int = 1
        registration: event_models.Registration
        for registration in registrations.all():
            serialized = RegistrationCashSummarySerializer(registration).data
            person: User = registration.responsible_persons.first()
            letter: StringAttribute = registration.tags.instance_of(StringAttribute).first()
            payement = serialized.get('payement', None)
            price = payement.get('price', 0) if payement else 0

            all_participants = self.get_participants(registration)
            participant_list = []
            participant: event_models.RegistrationParticipant
            for participant in all_participants.all():
                particpant_str = f'{participant.first_name} {participant.last_name}'
                participant_list.append(particpant_str)

            original[f'A{index + 1}'] = registration.scout_organisation.name
            original[f'B{index + 1}'] = person.first_name
            original[f'C{index + 1}'] = person.last_name
            original[f'D{index + 1}'] = person.email
            original[f'E{index + 1}'] = self.get_formatted_booking_option(registration, 'Bett')
            original[f'F{index + 1}'] = self.get_formatted_booking_option(registration, 'Zeltplatz')
            original[f'G{index + 1}'] = self.get_formatted_booking_option(registration, 'Tagesgast')
            original[f'H{index + 1}'] = serialized.get('participant_count', 0)
            original[f'I{index + 1}'] = price
            original[f'J{index + 1}'] = letter.string_field if letter else ''
            original[f'K{index + 1}'] = ',\n'.join(participant_list)
            original[f'L{index + 1}'] = f'{registration.event.name.replace(" ", "")[:10]}' \
                                        f'-{registration.scout_organisation.name.replace(" ", "")[:10]}' \
                                        f'-{str(registration.created_at.timestamp())[:10]}'
            index += 1

            return wb

    def get_formatted_booking_option(self, registration, booking_options_name):
        return registration.registrationparticipant_set.filter(booking_option__name=booking_options_name).count() or 0

    def get_participants(self, registration=None) -> QuerySet[event_models.RegistrationParticipant]:
        participants = event_models.RegistrationParticipant.objects.filter(registration=registration) \
            .order_by('last_name')
        return participants

    def get_registrations(self, event) -> QuerySet[event_models.Registration]:
        return event_models.Registration.objects.filter(event=event, is_confirmed=True)

    def get_event(self) -> event_models.Event:
        return self.generated_file.event
