import uuid

from django.db import models

from backend.storage_backends import PublicMediaStorage, EmailAttachmentMediaStorage
from basic import models as basic_models
from email_services import choices as email_choices


class EmailAttachment(basic_models.TimeStampMixin):
    id = models.UUIDField(auto_created=True, primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(storage=EmailAttachmentMediaStorage(), blank=True, null=True)


class EmailPicture(basic_models.TimeStampMixin):
    id = models.UUIDField(auto_created=True, primary_key=True, default=uuid.uuid4, editable=False)
    file = models.ImageField(storage=PublicMediaStorage())


class Email(basic_models.TimeStampMixin):
    id = models.UUIDField(auto_created=True, primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=60, null=True)
    html = models.TextField(default='')
    plain = models.TextField(default='')
    attachments = models.ManyToManyField(EmailAttachment, blank=True)
    type = models.CharField(max_length=20, choices=email_choices.EmailType.choices,
                            default=email_choices.EmailType.StandardEmail)

    def __str__(self):
        return f'{self.type}:{self.name}'


class StandardEmailSet(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=60)
    standard_email = models.ForeignKey(Email, on_delete=models.PROTECT,
                                       limit_choices_to={'type': email_choices.EmailType.StandardEmail},
                                       related_name='standard_email')
    event_created = models.ForeignKey(Email, on_delete=models.PROTECT,
                                      limit_choices_to={'type': email_choices.EmailType.EventCreated},
                                      related_name='event_created')
    event_updated = models.ForeignKey(Email, on_delete=models.PROTECT,
                                      limit_choices_to={'type': email_choices.EmailType.EventUpdated},
                                      related_name='event_updated')

    def __str__(self):
        return self.name


class StandardEmailRegistrationSet(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=60)
    registration_created = models.ForeignKey(Email, on_delete=models.PROTECT,
                                             limit_choices_to={'type': email_choices.EmailType.RegistrationCreated},
                                             related_name='registration_created',
                                             null=True, blank=True)
    registration_updated = models.ForeignKey(Email, on_delete=models.PROTECT,
                                             limit_choices_to={'type': email_choices.EmailType.RegistrationUpdated},
                                             related_name='registration_updated',
                                             null=True, blank=True)
    registration_reminder = models.ForeignKey(Email, on_delete=models.PROTECT,
                                              limit_choices_to={'type': email_choices.EmailType.RegistrationReminder},
                                              related_name='registration_reminder',
                                              null=True, blank=True)
    registration_accepted = models.ForeignKey(Email, on_delete=models.PROTECT,
                                              limit_choices_to={'type': email_choices.EmailType.RegistrationAccepted},
                                              related_name='registration_accepted',
                                              null=True, blank=True)
    payment_reminder = models.ForeignKey(Email, on_delete=models.PROTECT,
                                         limit_choices_to={'type': email_choices.EmailType.PaymentReminder},
                                         related_name='payment_reminder',
                                         null=True, blank=True)
    custom_mail = models.ForeignKey(Email, on_delete=models.PROTECT,
                                    limit_choices_to={'type': email_choices.EmailType.StandardEmail},
                                    related_name='custom_mail',
                                    null=True, blank=True)

    def __str__(self):
        return self.name
