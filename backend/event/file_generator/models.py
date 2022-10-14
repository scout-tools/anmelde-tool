import uuid
from django.contrib.auth.models import User
from django.db import models
from basic import models as basic_models
from event import models as event_models
from event.choices.choices import FileGenerationStatus, FileType, FileExtension
from backend.storage_backends import FileTemplateMediaStorage, GeneratedFilesStorage


class FileTemplate(models.Model):
    id = models.UUIDField(auto_created=True, primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(storage=FileTemplateMediaStorage)
    type = models.CharField(max_length=5, choices=FileType.choices, default=FileType.Kjp_complex)
    extension = models.CharField(max_length=1, choices=FileExtension.choices, default=FileExtension.Excel)
    version = models.IntegerField(default=1)


class GeneratedFiles(basic_models.TimeStampMixin):
    id = models.UUIDField(auto_created=True, primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(null=True, blank=True, storage=GeneratedFilesStorage)
    error_msg = models.CharField(max_length=10000, null=True, blank=True)
    status = models.CharField(max_length=2, choices=FileGenerationStatus.choices, default=FileGenerationStatus.Queued)
    event = models.ForeignKey(event_models.Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    extension = models.CharField(max_length=1, choices=FileExtension.choices, default=FileExtension.Excel)
    template = models.ForeignKey(FileTemplate, on_delete=models.SET_NULL, null=True)
