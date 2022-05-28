from event.file_generator.models import FileTemplate, GeneratedFiles


def pre_delete_file_template(sender, instance: FileTemplate, **kwargs):
    try:
        instance.file.delete(save=False)
    except FileTemplate.DoesNotExist:
        return


def pre_delete_generate_files(sender, instance: GeneratedFiles, **kwargs):
    try:
        instance.file.delete(save=False)
    except GeneratedFiles.DoesNotExist:
        return


def pre_save_file_template(sender, instance: FileTemplate, **kwargs):
    if not instance.pk:
        return

    try:
        old_file = FileTemplate.objects.get(pk=instance.pk).file
    except FileTemplate.DoesNotExist:
        return

    new_file = instance.file
    if not old_file == new_file:
        old_file.delete(save=False)
