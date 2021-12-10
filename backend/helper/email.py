from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
from django.template.loader import render_to_string
from pathlib import Path
from enum import Enum
import threading
from threading import Thread
from django.template.context import make_context
from django.template.loader import get_template

url = getattr(settings, 'FRONT_URL', '')
sender = f'Anmelde-Tool <{getattr(settings, "EMAIL_HOST_USER")}>'
email_directory = getattr(settings, 'TEMPLATES')[0]['DIRS'][0]


class MailType(Enum):
    Login = 0
    ForeignLogin = 1
    ResponsiblePerson = 2
    RegistrationSummary = 3
    RegistrationReminder = 4
    RegistrationMatching = 5


def get_mail(mail_type: MailType, data, email_id=0):
    if mail_type is MailType.Login:
        mail = 'login_mail'
    elif mail_type is MailType.ForeignLogin:
        mail = 'foreign_login_mail'
    elif mail_type is MailType.ResponsiblePerson:
        mail = 'responsible_person'
    elif mail_type is MailType.RegistrationSummary:
        mail = 'registration'
    elif mail_type is MailType.RegistrationReminder:
        if data['confirmed']:
            mail = 'reminder_mail'
        else:
            mail = 'reminder_mail_not_confirmed'
    elif mail_type is MailType.RegistrationMatching:
        if data['recipient_matched']:
            mail = 'matching'
        else:
            mail = 'matching_unmatched'
    else:
        return None

    if email_id != 0:
        path = f'{email_id}/{mail}'
        if not Path(f'{email_directory}/{path}.html').exists():
            path = f'default/{mail}'
    else:
        path = f'default/{mail}'

    project_tpl = get_template(f'{email_directory}/{path}.html')
    html_rendered = project_tpl.template.render(make_context(data, autoescape=False))
    plain_renderend = render_to_string(f'{path}.txt', data)
    # html_rendered = render_to_string(f'{path}.html', data)
    return plain_renderend, html_rendered


def send_auth_mail(user):
    user['mail'] = user['email']
    user['website'] = url

    plain_renderend, html_rendered = get_mail(MailType.Login, user)

    subject = "Willkommen beim Anmelde-Tool"
    recipients = [user['email']]

    return send_email(plain_renderend, html_rendered, subject, recipients)


def send_external_registration_mail(user, event_data):
    user['mail'] = user['email']
    user['website'] = url
    user['foreign_email'] = event_data['foreign_email']
    user['foreign_name'] = event_data['foreign_name']

    plain_renderend, html_rendered = get_mail(MailType.ForeignLogin, user, event_data['event_id'])

    subject = f"Willkommen beim Anmelde-Tool, du wurdest von {event_data['foreign_name']} registriert"
    recipients = [user['email']]

    return send_email(plain_renderend, html_rendered, subject, recipients)


def send_responsible_person_mail(data):
    plain_renderend, html_rendered = get_mail(MailType.ResponsiblePerson, data)

    subject = "Anmelde-Tool: Du wurdest einer Verantwortlichkeit zugewiesen"
    recipients = [data['email']]

    return send_email(plain_renderend, html_rendered, subject, recipients)


def send_registration_summary(data):
    plain_renderend, html_rendered = get_mail(MailType.RegistrationSummary, data, data['email_id'])

    subject = "Anmelde-Tool: Anmeldung abgeschlossen"
    recipients = [data['email']]

    return send_email(plain_renderend, html_rendered, subject, recipients)


def send_registration_reminder(data):
    plain_renderend, html_rendered = get_mail(MailType.RegistrationReminder, data, data['email_id'])

    if data['confirmed']:
        subject = "Erinnerung: Deine Registrierung beim stadt&spiel"
    else:
        subject = "Erinnerung: Deine unvollständige Registrierung beim stadt&spiel. Bitte bestätigen!"

    recipients = [data['email']]

    return send_email(plain_renderend, html_rendered, subject, recipients)


def send_matching(data):
    plain_renderend, html_rendered = get_mail(MailType.RegistrationMatching, data, data['email_id'])

    subject = "Neuigkeiten vom stadt&spiel"

    recipients = [data['email']]
    attachments = ('Checkliste.pdf', 'Einladung.docx', 'stadt&spiel_Packliste.docx', 'Zeitplan.pdf')
    return send_email(plain_renderend, html_rendered, subject, recipients, reply_to=('stadt@bdp-dpv.de',),
                      attachments=attachments)


def send_simple(data):
    subject = f"Neuigkeiten vom {data['event']}"
    recipients = data['email']
    if data['reply_to'] is not None:
        return send_email(data['text'], "", subject, recipients, reply_to=data['reply_to'], simple=True)
    else:
        return send_email(data['text'], "", subject, recipients, simple=True)


def send_email(plain_renderend, html_rendered, subject, recipients, reply_to=('support@anmelde-tool.de',),
               attachments=[], simple=False):
    EmailComplexThread(plain_renderend, html_rendered, subject, recipients, reply_to, attachments, simple).start()


class EmailComplexThread(threading.Thread):
    def __init__(self, body_plain, body_html, subject, recipients, reply_to, attachments, simple=False):
        self.subject = subject
        self.recipient_list = recipients
        self.html_content = body_html
        self.body_plain = body_plain
        self.reply_to = reply_to
        self.attachments = attachments
        self.simple = simple
        threading.Thread.__init__(self)

    def run(self):
        if self.simple:
            email = EmailMessage(self.subject, self.body_plain, sender, self.recipient_list,
                                 bcc=[getattr(settings, "EMAIL_HOST_USER")], reply_to=self.reply_to)
        else:
            email = EmailMultiAlternatives(self.subject, self.html_content, sender, self.recipient_list,
                                           bcc=[getattr(settings, "EMAIL_HOST_USER")],
                                           reply_to=self.reply_to)
            email.content_subtype = 'html'

        for atm in self.attachments:
            path = Path(f'{email_directory}/attachments/{atm}')
            if path.exists():
                email.attach_file(path)

        email.send()
