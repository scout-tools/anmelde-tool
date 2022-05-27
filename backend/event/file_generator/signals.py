from event.file_generator.models import FileTemplate, GeneratedFiles


def pre_delete_file_template(sender, instance: FileTemplate, **kwargs):
    instance.file.delete(save=False)


def pre_delete_generate_files(sender, instance: GeneratedFiles, **kwargs):
    instance.file.delete(save=False)
