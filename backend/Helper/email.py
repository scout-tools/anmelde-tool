from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

url = getattr(settings, 'FRONT_URL', '')
sender = f'BdP DPV Aktion <{getattr(settings, "EMAIL_HOST_USER")}>'


def send_auth_mail(user):
    context = {'user': user['user'], 'username': user['username'], 'mail': user['email'], 'website': url,
               'password': user['password']}

    plain_renderend = render_to_string('token_mail/token_mail.txt', context)
    html_rendered = render_to_string('token_mail/token_mail.html', context)

    subject = "Willkommen bei der BdP DPV Aktion"
    recipients = [user['email']]

    try:
        send_email(plain_renderend, html_rendered, subject, recipients)
        return "Email Is Sent"
    except Exception as e:
        print("Email not sent ", e)


def send_external_registration_mail(user):
    context = {'user': user['user'], 'username': user['username'], 'mail': user['email'], 'website': url,
               'password': user['password']}

    plain_renderend = render_to_string('token_mail/token_mail.txt', context)
    html_rendered = render_to_string('token_mail/token_mail.html', context)

    subject = "Willkommen bei der BdP DPV Aktion, du wurdest registriert"
    recipients = [user['email']]

    try:
        send_email(plain_renderend, html_rendered, subject, recipients)
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
