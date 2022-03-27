from event import models as event_models
from email_services import services


def pre_delete_registration(sender, instance: event_models.Registration, **kwargs):
    for tag in instance.tags.all():
        tag.delete()


def post_save_registation(sender: event_models.Registration,
                          instance: event_models.Registration,
                          update_fields,
                          raw,
                          **kwargs):
    if 'is_confirmed' in update_fields and instance.is_confirmed:
        services.send_registration_created_mail(instance_id=str(instance.id))
