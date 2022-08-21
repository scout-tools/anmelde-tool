from backend import settings
from .choices import EmailType
from .threads.registration import registration_confirmed_mail
from .threads.payment_reminder import payment_reminder_mail

url = getattr(settings, 'FRONT_URL', '')
email_active = getattr(settings, 'SEND_MAIL', False)


def send_registration_created_mail(**kwargs):
    instance_id = kwargs.get('instance_id')
    if instance_id and email_active:
        registration_confirmed_mail.delay(instance_id, EmailType.RegistrationCreated)


def send_payment_reminder_mail(event_id):
    if email_active:
        payment_reminder_mail.delay(event_id, EmailType.PaymentReminder)
