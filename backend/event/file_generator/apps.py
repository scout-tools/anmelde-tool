from django.apps import AppConfig
from django.db.models.signals import pre_delete


class FileGeneratorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'event.file_generator'

    def ready(self):
        from event.file_generator.models import FileTemplate, GeneratedFiles
        from event.file_generator.signals import pre_delete_generate_files, pre_delete_file_template
        pre_delete.connect(pre_delete_generate_files, sender=GeneratedFiles, dispatch_uid="pre_delete_generate_files")
        pre_delete.connect(pre_delete_file_template, sender=FileTemplate, dispatch_uid="pre_delete_file_template")

        from event.file_generator.file_generators import FileGeneratorDeqeueThread
        generator_deqeue_thread = FileGeneratorDeqeueThread()
        generator_deqeue_thread.daemon = True
        generator_deqeue_thread.start()
