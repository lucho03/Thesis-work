from re import search
from mysite import settings
from .models import TicketModel, AnswerModel, CommentAnswerModel
from email_listener import EmailListener
from threading import Thread
from django.contrib.auth.models import User
from django.core.mail import send_mail

from emailpy import EmailManager

dir = "Inbox"
attachment_dir = "./media"
emails = EmailListener(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD, dir, attachment_dir)
emails.login()

def check_emails():
    #Heroku work on 550 hours
    timeout = 550*60
    t = Thread(target=emails.listen, args=[timeout, create_ticket])
    t.start()

def send_meeting_email(title, meet, reciever):
    send_mail(
        'Video call about \' ' + reduction(title) + '\' ',
        'Our agent want to meet you \nPlease follow this link ' + meet,
        settings.EMAIL_HOST_USER,
        [reciever],
        fail_silently=False
    )

def send_erasing_email(title, text, reason, agent, receiver):
    send_mail(
        'Your ticket \'' + reduction(title) + '\' was deleted!',
        'Ticket: ' + text + '\nReason: ' + reason + '\nDeleted by ' + agent,
        settings.EMAIL_HOST_USER,
        [receiver],
        fail_silently=False
    )

def send_answering_email(title, id, text, answer, agent, receiver):
    send_mail(
        'You have an answer of \'' + reduction(title) + '\'',
        'ID: ' + str(id) + '\nTicket: ' + text + '\n\nAnswer: ' + answer + '\nSent by ' + agent,
        settings.EMAIL_HOST_USER,
        [receiver],
        fail_silently=False
    )

def send_invitation_email(receiver):
    send_mail(
        'Invitation',
        'Hello, \nYou have an invitation to join our team. \nPlease open this registration form: https://protected-cliffs-91463.herokuapp.com/register_agent' + str(settings.REGISTER_AGENT_URL),
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
        if 'Re: ' in title:
            try:
                result = search('ID: (.*)\n', text)
                answer = AnswerModel.objects.get(pk=result.group(1))
                arr = text.split('=')
                answer.answer_comments += 1
                comment = CommentAnswerModel.objects.create(
                                                            answer=answer, 
                                                            author='Email', 
                                                            text=arr[0], 
                                                            number=answer.answer_comments
                                                            )
                answer.save()
                comment.save()
            except Exception:
                print('Invalid response sent!')
                pass
        else:
            ticket = TicketModel.objects.create(author=User.objects.create(
                                                                            username=name, 
                                                                            email=author_email
                                                                            )
                                                )
            if len(text) == 0:
                return
            else:
                ticket.title = title
                ticket.text = text
                try:
                    ticket.file = messages[key].get('attachments')[0].replace('./media/', '')
                except Exception:
                    pass
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