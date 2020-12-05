from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.conf import settings
from django.core.mail import send_mail

url = getattr(settings, 'FRONT_URL', '')
sender = getattr(settings, 'EMAIL_HOST_USER')


def send_register_mail(user, key):
    body = """
    Hello %s
    Confirmation Mail: %s
    You can see more details in this link: %s/account-confirm-email/%s <br><br>
    Thank you <br><br>
    <p>
    """ % (user.first_name, user.email, url, key)

    subject = "Registeration Confirmation Mail"
    recipients = [user.email]

    try:
        send_email(body, subject, recipients, 'html')
        return "Email Is Sent"
    except Exception as e:
        print("Email not sent ", e)


def send_reset_password_email(user):
    body = """
    hello %s,
    Reset Mail Link : %s/%s/%s
    """ % (user.username, url, urlsafe_base64_encode(force_bytes(user.pk)), default_token_generator.make_token(user))
    subject = "Reset password Mail"
    recipients = [user.email]
    try:
        send_email(body, subject, recipients, 'html')
        return "Email Is Sent"
    except Exception as e:
        print("Email not sent ", e)


def send_email(body, subject, recipients, body_type='plain'):
    send_mail(
        subject,
        body,
        sender,
        recipients,
        fail_silently=False,
    )
