from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.template.loader import get_template
from django.template import Context

url = getattr(settings, 'FRONT_URL', '')
sender = f'BdP DPV Aktion <{getattr(settings, "EMAIL_HOST_USER" )}>'


def send_register_mail(user, key):
    context = {'username': user.username, 'mail': user.email, 'website': url, 'token': key}

    plain_renderend = render_to_string('token_mail.txt', context)
    html_rendered = render_to_string('token_mail.html', context)

    print(key)
    subject = "Registeration Confirmation Mail"
    recipients = [user.email]

    try:
        send_email(plain_renderend, html_rendered, subject, recipients)
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


def send_email(body_plain, body_html, subject, recipients):
    send_mail(
        subject,
        body_plain,
        sender,
        recipients,
        fail_silently=False,
        html_message=body_html,
    )
