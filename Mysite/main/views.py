import django
from django.core.paginator import Paginator
from django.http import FileResponse, HttpResponseForbidden, HttpResponseNotFound
from django.urls import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import TemplateView

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.auth.decorators import login_required, permission_required

from .forms import AnswerModelForm, TicketModelForm, UserForm, AgentForm
from .models import AnswerModel, TicketModel, CommentTicketModel, CommentAnswerModel
from .emails import check_emails, send_erasing_email, send_answering_email, send_meeting_email

# check_emails()

class View(TemplateView):
    def main_page(request):
        if isinstance(request.user, AnonymousUser):
            return render(request, 'main_page.html')
        else:
            return HttpResponseRedirect('/dashboard')
        
    
    def register_agent(request):
        kind = 1
        if isinstance(request.user, User):
            return HttpResponseRedirect('/dashboard')
        if request.method == 'POST':
            form = AgentForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return HttpResponseRedirect('/dashboard')
        else:
            form = AgentForm()
        return render(request, 'login_user.html', {'form': form, 'kind':kind})
    
    def register(request):
        kind = 2
        if isinstance(request.user, User):
            return HttpResponseRedirect('/dashboard')
        if request.method == 'POST':
            form = UserForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return HttpResponseRedirect('/dashboard')
        else:
            form = UserForm()
        return render(request, 'login_user.html', {'form': form, 'kind':kind})
    
    def logout_user(request):
        logout(request)
        return HttpResponseRedirect('/')
    
    def log_in(request):
        kind = 3
        if isinstance(request.user, User):
            return HttpResponseRedirect('/dashboard')
        if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid:
                username = form.data['username']
                password = form.data['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect('/dashboard')
                elif User.objects.filter(username=username).exists() == False:
                    messages.error(request, 'Wrong username')
                else:
                    messages.error(request, 'Wrong password')
        form = AuthenticationForm()
        return render(request, 'login_user.html', {'form': form, 'kind':kind})
    
    @login_required(login_url='/log_in')
    def dashboard(request):
        tickets = None
        if request.user.has_perm('main.create_tickets'):
            tickets = TicketModel.objects.all().filter(author=request.user).exclude(status='C').order_by('priority')
        if request.user.has_perm('main.answer_tickets'):
            tickets = TicketModel.objects.all().exclude(status='C').order_by('priority')
        return render(request, 'dashboard.html', {'tickets':tickets})
    
    @login_required(login_url='/log_in')
    def profile(request):
        if request.method == 'POST':
            if len(request.POST.get('change-username')) > 0:
                new_username = request.POST.get('change-username')
                if User.objects.filter(username=new_username).exists() == True:
                    messages.error(request, 'This username is in use')
                else:
                    request.user.username = request.POST.get('change-username')
            
            if len(request.POST.get('change-email')) > 0:
                request.user.email = request.POST.get('change-email')
            if len(request.POST.get('change-first-name')) > 0:
                request.user.first_name = request.POST.get('change-first-name')
            if len(request.POST.get('change-last-name')) > 0:
                request.user.last_name = request.POST.get('change-last-name')
            request.user.save()
        num_tickets = TicketModel.objects.all().filter(author=request.user).count()
        return render(request, 'profile.html', {'tickets':num_tickets})

@login_required(login_url='/log_in')
class Tickets(TemplateView):
    @permission_required('main.create_tickets', raise_exception=True)
    def set_ticket(request):
        form = TicketModelForm(request.POST, request.FILES)
        if request.method == 'POST':
            if form.is_valid():
                if len(form.data.get('text')) == 0:
                    messages.error(request, 'Empty ticket!')
                elif len(form.data.get('title')) == 0:
                    messages.error(request, 'Empty title!')
                else:
                    curr = form.save(commit=False)
                    curr.author = request.user
                    if request.FILES.get('file-name') is not None:
                        if TicketModel.objects.filter(file=request.FILES.get('file-name')).exists() == True:
                            messages.error(request, 'File with that name already exists')
                            return render(request, 'send_ticket.html', {'form':form})
                        else:
                            curr.file = request.FILES.get('file-name')
                    curr.save()
                    return HttpResponseRedirect('/dashboard')
        return render(request, 'send_ticket.html', {'form':form})
    
    @permission_required('main.create_tickets', raise_exception=True)
    def get_tickets(request):
        tickets = TicketModel.objects.all().filter(author=request.user).order_by('priority')
        comments = CommentTicketModel.objects.all()
        if request.POST.get('change') is not None:
            id = int(request.POST.get('change'))
            return HttpResponseRedirect(reverse('rewrite', kwargs={'id':id}))
        if request.POST.get('answers') is not None:
            id = int(request.POST.get('answers'))
            return HttpResponseRedirect(reverse('view_answers', kwargs={'id':id}))
        if request.POST.get('comment') is not None:
            id = int(request.POST.get('comment'))
            ticket = tickets.get(id=id)
            ticket.ticket_comments += 1
            comment = CommentTicketModel.objects.create(
                                                        ticket=ticket, 
                                                        text=request.POST.get('more-info'), 
                                                        number=ticket.ticket_comments
                                                        )
            comment.save()
            ticket.save()
        if request.POST.get('file-button-name') is not None:
            id = int(request.POST.get('file-button-name'))
            ticket = tickets.get(id=id)
            filepath = str(ticket.file)
            try:
                return FileResponse(open('media/' + filepath, 'rb'))
            except Exception:
                return HttpResponseNotFound('<h1><strong>File not found</strong></h1>')
        return render(request, 'tickets.html', {'tickets':tickets, 'comments':comments})
    
    @permission_required('main.create_tickets', raise_exception=True)
    def rewrite(request, id):
        ticket = TicketModel.objects.get(pk=id)
        form = TicketModelForm(request.POST or None, instance=ticket)
        if form.is_valid():
            if len(form.data.get('text')) == 0:
                messages.error(request, 'Empty ticket!')
            elif len(form.data.get('title')) == 0:
                messages.error(request, 'Empty title!')
            else:
                form.save()
                return HttpResponseRedirect('/tickets')
        return render(request, 'send_ticket.html', {'ticket':ticket, 'form':form})
    
    @permission_required('main.create_tickets', raise_exception=True)
    def view_answers(request, id):
        ticket = TicketModel.objects.get(pk=id)
        answers = AnswerModel.objects.all().filter(ticket=ticket).order_by('number')
        comments = CommentAnswerModel.objects.all()
        if request.POST.get('comment') is not None:
            id = int(request.POST.get('comment'))
            answer = answers.get(id=id)
            if answer.lock == True:
                if answer.author != request.user:
                    return HttpResponseForbidden('<h1><strong>Forbidden action!</strong></h1>')
            answer.answer_comments += 1
            comment = CommentAnswerModel.objects.create(
                                                        answer=answer, 
                                                        author=request.user.username, 
                                                        text=request.POST.get('more'), 
                                                        number=answer.answer_comments
                                                        )
            comment.save()
            answer.save()
        return render(request, 'answer.html', {'ticket':ticket, 'answers':answers, 'comments':comments})
    
    @permission_required('main.answer_tickets', raise_exception=True)
    def list_tickets(request):
        tickets = TicketModel.objects.all().exclude(status='C').order_by('priority')
        comments = CommentTicketModel.objects.all()
        if request.POST.get('answer') is not None:
            id = int(request.POST.get('answer'))
            return HttpResponseRedirect(reverse('answer', kwargs={'id':id}))
        if request.POST.get('delete') is not None:
            id = int(request.POST.get('delete'))
            ticket = tickets.get(id=id)
            # send_erasing_email(
            #                     ticket.title, 
            #                     ticket.clear_text(), 
            #                     request.POST.get('because'), -
            #                     request.user.username, 
            #                     ticket.author.email
            #                     )
            ticket.delete()
            return HttpResponseRedirect('/dashboard')
        if request.POST.get('file-button-name') is not None:
            id = int(request.POST.get('file-button-name'))
            ticket = tickets.get(id=id)
            filepath = str(ticket.file)
            try:
                return FileResponse(open('media/' + filepath, 'rb'))
            except Exception:
                return HttpResponseNotFound('<h1><strong>File not found</strong></h1>')
        if request.POST.get('meeting') is not None:
            id = int(request.POST.get('meeting'))
            ticket = tickets.get(id=id)
            # send_meeting_email(ticket.title, request.POST.get('meet'), ticket.author.email)
        return render(request, 'tickets.html', {'tickets':tickets, 'comments':comments})
    
    @permission_required('main.answer_tickets', raise_exception=True)
    def answer(request, id):
        ticket = TicketModel.objects.get(pk=id)
        answers = AnswerModel.objects.all().filter(ticket=ticket).order_by('number')
        comments = CommentAnswerModel.objects.all()
        if ticket.status == 'C':
            return render(request, 'answer.html', {'ticket':ticket, 'answers':answers, 'comments':comments})

        form = AnswerModelForm(request.POST)
        if request.method == 'POST':
            if request.POST.get('comment') is not None:
                id = int(request.POST.get('comment'))
                answer = answers.get(id=id)
                if answer.lock == True:
                    if answer.author != request.user:
                        return HttpResponseForbidden('<h1><strong>Forbidden action!</strong></h1>')
                answer.answer_comments += 1
                comment = CommentAnswerModel.objects.create(
                                                                answer=answer, 
                                                                author=request.user.username, 
                                                                text=request.POST.get('more'), 
                                                                number=answer.answer_comments
                                                            )
                answer.save()
                comment.save()
                return HttpResponseRedirect('/answer/{}'.format(ticket.id))
            if request.POST.get('close_ticket') is not None:
                id = int(request.POST.get('close_ticket'))
                ticket = TicketModel.objects.get(pk=id)
                ticket.status = 'C'
                ticket.save()
                return HttpResponseRedirect('/dashboard')
            if form.is_valid():
                if len(form.data.get('text')) == 0:
                    messages.error(request, 'Empty answer!')
                elif len(form.data.get('title')) == 0:
                    messages.error(request, 'Empty title!')
                else:
                    curr = form.save(commit=False)
                    curr.author = request.user
                    curr.ticket = ticket
                    ticket.num_answers += 1
                    ticket.status = 'O'
                    curr.number = ticket.num_answers
                    if request.POST.get('lock-button') is not None:
                        curr.lock = True
                    curr.save()
                    ticket.save()
                    # if request.POST.get('send_to_mail') == 'yes' or ticket.is_from_email():
                        # send_answering_email(
                        #                         ticket.title, 
                        #                         curr.id, 
                        #                         ticket.clear_text(), 
                        #                         curr.clear_text(), 
                        #                         request.user.username, 
                        #                         ticket.author.email
                        #                     )
                    return HttpResponseRedirect('/answer/'+str(ticket.id)+'#ticket-answer-'+str(curr.number))
        return render(request, 'answer.html', {'ticket':ticket, 'form':form, 'answers':answers, 'comments':comments})
    
    @permission_required('main.answer_tickets', raise_exception=True)
    def knowledge_base(request):
        tickets = TicketModel.objects.all().filter(status='C').order_by('priority')
        comments = CommentTicketModel.objects.all()
        if tickets.count() <= 3:
            object = tickets
        else:
            paginator = Paginator(tickets, 3)
            page_number = request.GET.get('page')
            object = paginator.get_page(page_number)
        if request.POST.get('file-button-name') is not None:
            id = int(request.POST.get('file-button-name'))
            ticket = tickets.get(id=id)
            filepath = str(ticket.file)
            try:
                return FileResponse(open('media/' + filepath, 'rb'))
            except Exception:
                return HttpResponseNotFound('<h1><strong>File not found</strong></h1>')
        if request.POST.get('delete') is not None:
            id = int(request.POST.get('delete'))
            ticket = tickets.get(id=id)
            ticket.delete()
            if isinstance(object, django.core.paginator.Page):
                return HttpResponseRedirect('/knowledge_base?page=' + str(object.number))
            else:
                return HttpResponseRedirect('/knowledge_base')
        if request.POST.get('answers') is not None:
            id = int(request.POST.get('answers'))
            return HttpResponseRedirect(reverse('answer', kwargs={'id':id}))
        return render(request, 'knowledge_base.html', {'tickets':object, 'comments':comments})
