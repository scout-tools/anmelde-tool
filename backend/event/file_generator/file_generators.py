import os
import time
import traceback
from tempfile import NamedTemporaryFile

from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.files.base import File
from event.file_generator.generators.attribute_generator import AttributeGenerator
from event.file_generator.generators.kjr_generator import KjrGenerator
from event.file_generator.generators.travel_matrix_generator import TravelMatrixGenerator

from event.choices.choices import FileGenerationStatus, FileType, FileExtension
from event.file_generator.generators.abstract_generator import AbstractGenerator
from event.file_generator.generators.invoice_generator import InvoiceGenerator
from event.file_generator.generators.kjp_generator import KjpGenerator
from event.file_generator.generators.participant_generator import ParticipantGenerator
from event.file_generator.models import GeneratedFiles

logger = get_task_logger(__name__)


@shared_task()
def generate_file(instance_id):
    file_wrapper = GeneratedFiles.objects.get(pk=instance_id)
    file_wrapper.status = FileGenerationStatus.Processing
    file_wrapper.save()
    try:
        generator: AbstractGenerator = None
        if file_wrapper.template.type == FileType.Kjp \
                and file_wrapper.extension == FileExtension.Excel \
                and file_wrapper.template.version == 1:
            generator = KjpGenerator(file_wrapper)

        elif file_wrapper.template.type == FileType.Invoice \
                and file_wrapper.extension == FileExtension.Excel \
                and file_wrapper.template.version == 1:
            generator = InvoiceGenerator(file_wrapper)

        elif file_wrapper.template.type == FileType.ParticipantList \
                and file_wrapper.extension == FileExtension.Excel \
                and file_wrapper.template.version == 1:
            generator = ParticipantGenerator(file_wrapper)

        elif file_wrapper.template.type == FileType.AttributeList \
                and file_wrapper.extension == FileExtension.Excel \
                and file_wrapper.template.version == 1:
            generator = AttributeGenerator(file_wrapper)

        elif file_wrapper.template.type == FileType.TravelMatrix \
                and file_wrapper.extension == FileExtension.Excel \
                and file_wrapper.template.version == 1:
            generator = TravelMatrixGenerator(file_wrapper)

        elif file_wrapper.template.type == FileType.KJR \
                and file_wrapper.extension == FileExtension.Excel \
                and file_wrapper.template.version == 1:
            generator = KjrGenerator(file_wrapper)

        if generator is not None:
            wb = generator.generate()
            save_file_excel(file_wrapper, wb)
        else:
            logger.debug(f'No suitable template found for generated file {file_wrapper.id}: {file_wrapper.template}')
    except Exception as e:
        file_wrapper.error_msg = f'{e}\n{traceback.format_exc()}'
        file_wrapper.status = FileGenerationStatus.FinishedFailed
    else:
        file_wrapper.status = FileGenerationStatus.FinishedSuccessfull
    file_wrapper.save()
    return True


def save_file_excel(file_wrapper, wb):
    temp_file = NamedTemporaryFile(suffix=".xlsx", delete=False)
    wb.save(temp_file.name)
    temp_file.seek(0)
    file_name = f'{file_wrapper.template.get_type_display()}_{time.time()}.xlsx'
    file_wrapper.file.save(file_name, File(temp_file))
    temp_file.close()
    os.remove(temp_file.name)
