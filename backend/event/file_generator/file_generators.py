import os
import threading
import time
import traceback
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.files.base import File
from tempfile import NamedTemporaryFile
from backend import settings
from event.file_generator.models import GeneratedFiles
from event.choices.choices import FileGenerationStatus, FileType, FileExtension
from event.file_generator.generators.abstract_generator import AbstractGenerator
from event.file_generator.generators.kjp_generator_easy import KjpGeneratorEasy
from event.file_generator.generators.kjr_generator import KjrGenerator
from event.file_generator.generators.travel_matrix_generator import TravelMatrixGenerator
from event.file_generator.generators.kjp_generator_complex import KjpGeneratorComplex
from event.file_generator.generators.invoice_generator import InvoiceGenerator
from event.file_generator.generators.participant_generator import ParticipantGenerator
from event.file_generator.generators.attribute_generator import AttributeGenerator

timer = getattr(settings, 'FILE_GENERATOR_DEQEUE_TIME', 60)
debug = getattr(settings, 'DEBUG', False)


class FileGeneratorDeqeueThread(threading.Thread):

    def run(self) -> None:
        print('Starting file generator thread')
        while True:
            try:
                time.sleep(timer)
                timed_out = datetime.now(tz=timezone.get_current_timezone()) - timedelta(minutes=5)
                GeneratedFiles.objects.filter(status=FileGenerationStatus.Processing, updated_at__lt=timed_out) \
                    .update(status=FileGenerationStatus.FinishedFailed, error_msg='Timeout reached')

                unprocessed = GeneratedFiles.objects.filter(status=FileGenerationStatus.Queued).order_by('-created_at')
                processing = GeneratedFiles.objects.filter(status=FileGenerationStatus.Processing)

                if unprocessed.exists() and not processing.exists():
                    file_to_be_generated = unprocessed.last()
                    generator_thread = FileGeneratorThread(file_to_be_generated)
                    if debug:
                        generator_thread.run()
                    else:
                        generator_thread.daemon = True
                        generator_thread.start()
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
            generator: AbstractGenerator = None
            if self.generated_file.template.type == FileType.Kjp_complex \
                    and self.generated_file.extension == FileExtension.Excel \
                    and self.generated_file.template.version == 1:
                generator = KjpGeneratorComplex(self.generated_file)

            elif self.generated_file.template.type == FileType.Kjp_easy \
                    and self.generated_file.extension == FileExtension.Excel \
                    and self.generated_file.template.version == 1:
                generator = KjpGeneratorEasy(self.generated_file)

            elif self.generated_file.template.type == FileType.Invoice \
                    and self.generated_file.extension == FileExtension.Excel \
                    and self.generated_file.template.version == 1:
                generator = InvoiceGenerator(self.generated_file)

            elif self.generated_file.template.type == FileType.ParticipantList \
                    and self.generated_file.extension == FileExtension.Excel \
                    and self.generated_file.template.version == 1:
                generator = ParticipantGenerator(self.generated_file)

            elif self.generated_file.template.type == FileType.AttributeList \
                    and self.generated_file.extension == FileExtension.Excel \
                    and self.generated_file.template.version == 1:
                generator = AttributeGenerator(self.generated_file)

            elif self.generated_file.template.type == FileType.TravelMatrix \
                    and self.generated_file.extension == FileExtension.Excel \
                    and self.generated_file.template.version == 1:
                generator = TravelMatrixGenerator(self.generated_file)

            elif self.generated_file.template.type == FileType.KJR \
                    and self.generated_file.extension == FileExtension.Excel \
                    and self.generated_file.template.version == 1:
                generator = KjrGenerator(self.generated_file)

            if generator is not None:
                wb = generator.generate()
                self.save_file_excel(wb)
            else:
                raise Exception('Kein geeignetes Template gefunden.')
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            self.generated_file.error_msg = traceback.format_exc()
            self.generated_file.status = FileGenerationStatus.FinishedFailed
        else:
            self.generated_file.status = FileGenerationStatus.FinishedSuccessfully
        self.generated_file.save()

    def save_file_excel(self, wb):
        temp_file = NamedTemporaryFile(suffix=".xlsx", delete=False)
        wb.save(temp_file.name)
        temp_file.seek(0)
        file_name = f'{self.generated_file.template.get_type_display()}_{time.time()}.xlsx'
        self.generated_file.file.save(file_name, File(temp_file))
        temp_file.close()
        os.remove(temp_file.name)
