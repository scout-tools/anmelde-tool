import os
import threading
import time
import uuid
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import QuerySet
from dateutil.relativedelta import relativedelta
from openpyxl import load_workbook
from django.core.files.base import File
from tempfile import NamedTemporaryFile
from queue import Queue
from backend import settings
from event.choices.choices import FileGenerationStatus, FileType, FileExtension
from event.file_generator.models import FileTemplate, GeneratedFiles
from event import models as event_models
from event.file_generator.serializers import GeneratedFilesGetSerializer

timer = getattr(settings, 'FILE_GENERATOR_DEQEUE_TIME', 60)


class FileGeneratorDeqeueThread(threading.Thread):

    def run(self) -> None:
        print('Starting file generator thread')
        while True:
            try:
                time.sleep(timer)
                timed_out = datetime.now(tz=timezone.get_current_timezone()) - timedelta(minutes=5)
                GeneratedFiles.objects.filter(status=FileGenerationStatus.Processing, updated_at__lt=timed_out) \
                    .update(status=FileGenerationStatus.FinishedFailed, error_msg='Timeout reached')

                unprocessed = GeneratedFiles.objects.filter(status=FileGenerationStatus.Queued)
                processing = GeneratedFiles.objects.filter(status=FileGenerationStatus.Processing)

                if unprocessed.exists() and not processing.exists():
                    file_to_be_generated = unprocessed.first()
                    FileGeneratorThread(file_to_be_generated).start()
            except RuntimeError as e:
                print(e)


class FileGeneratorThread(threading.Thread):
    def __init__(self, generated_file: GeneratedFiles):
        super().__init__()
        self.generated_file = generated_file

    def run(self) -> None:
        self.generated_file.status = FileGenerationStatus.Processing
        self.generated_file.save()
        try:
            if self.generated_file.type == FileType.Kjp and self.generated_file.extension == FileExtension.Excel:
                self.generate_kjp_excel()
        except Exception as e:
            print(e)
            self.generated_file.error_msg = e
            self.generated_file.status = FileGenerationStatus.FinishedFailed
        else:
            self.generated_file.status = FileGenerationStatus.FinishedSuccessfull
        self.generated_file.save()

    def generate_kjp_excel(self):
        event: event_models.Event = self.get_event()
        participants = self.get_participants(event)
        file = FileTemplate.objects.first()
        wb = load_workbook(file.file)
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

        temp_file = NamedTemporaryFile(suffix=".xlsx", delete=False)
        wb.save(temp_file.name)
        temp_file.seek(0)
        self.generated_file.file.save(f'KJP_{time.time()}.xlsx', File(temp_file))
        temp_file.close()
        os.remove(temp_file.name)

    def get_participants(self, event) -> QuerySet[event_models.RegistrationParticipant]:
        registrations = event_models.Registration.objects.filter(event=event, is_confirmed=True) \
            .values_list('id', flat=True)
        participants = event_models.RegistrationParticipant.objects.filter(registration__in=registrations) \
            .order_by('last_name')
        return participants

    def get_event(self) -> event_models.Event:
        return self.generated_file.event
