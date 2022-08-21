from django.apps import AppConfig
from django.db.models.signals import pre_delete, pre_save, post_save


class FileGeneratorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'event.file_generator'

    def ready(self):
        from event.file_generator.models import FileTemplate, GeneratedFiles
        from event.file_generator.signals import pre_delete_generate_files, pre_delete_file_template, \
            pre_save_file_template, post_save_generate_files
        pre_delete.connect(pre_delete_generate_files, sender=GeneratedFiles, dispatch_uid='pre_delete_generate_files')
        pre_delete.connect(pre_delete_file_template, sender=FileTemplate, dispatch_uid='pre_delete_file_template')
        pre_save.connect(pre_save_file_template, sender=FileTemplate, dispatch_uid='pre_save_file_template')
        post_save.connect(post_save_generate_files, sender=GeneratedFiles, dispatch_uid='post_delete_generate_files')
