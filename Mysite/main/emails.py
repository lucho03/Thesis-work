from mysite import settings
from .models import TicketModel
from email_listener import EmailListener
from threading import Thread
from django.contrib.auth.models import User
from django.core.mail import send_mail

from emailpy import EmailManager

dir = "Inbox"
attachment_dir = "./main/static/emails_folder"
emails = EmailListener(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD, dir, attachment_dir)
emails.login()

def check_emails():
    timeout = 550*60
    t = Thread(target=emails.listen, args=[timeout, create_ticket])
    t.start()

def send_erasing_email(title, text, reason, agent, receiver):
    send_mail(
        'Your ticket \'' + reduction(title) + '\' was deleted!',
        'Ticket: ' + text + '\nReason: ' + reason + '\nDeleted by ' + agent,
        settings.EMAIL_HOST_USER,
        [receiver],
        fail_silently=False
    )

def send_answering_email(title, text, answer, agent, receiver):
    send_mail(
        'You have an answer of \'' + reduction(title) + '\'',
        'Ticket: ' + text + '\n\nAnswer: ' + answer + '\nSent by ' + agent,
        settings.EMAIL_HOST_USER,
        [receiver],
        fail_silently=False
    )

def create_ticket(email_listener, messages):
    for key in messages.keys():
        name = key.split('_')[0]
        author_email = key.split('_')[1]
        title = messages[key].get('Subject')
        text = messages[key].get('Plain_Text')
        ticket = TicketModel.objects.create(author=User.objects.create(username=name, email=author_email))
        if len(text) == 0:
            return
        else:
            ticket.title = title
            ticket.text = text
            if 'problem' or 'Problem' in text:
                ticket.type = 'P'
                ticket.priority = '2'
            ticket.save()

def check_emails2():
    manager = EmailManager(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    messages = manager.read()
    for message in messages:
        print(message.sender, message.subject, message.body, message.attachments)

def print_email(email_listener, messages):
    for key in messages.keys():
        print(key)
        print(messages[key])
        print(messages[key].get('Subject'))
        print(messages[key].get('Plain_Text'))

def reduction(str):
    if len(str) <= 12:
        return str
    else:
        dots = '...'
        return str[0:12] + dots