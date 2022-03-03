from django.core.paginator import Paginator
from django.http import FileResponse
from django.urls import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import TemplateView

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import login_required, permission_required
from pyparsing import empty

from .forms import AnswerModelForm, TicketModelForm, UserForm, AgentForm
from .models import AnswerModel, TicketModel, CommentTicketModel, CommentAnswerModel
from .emails import check_emails, send_erasing_email, send_answering_email

#check_emails()

class View(TemplateView):
    def main_page(request):
        return render(request, 'main_page.html')
    
    def register_agent(request):
        print("Proba")
        if request.method == 'POST':
            form = AgentForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.user_permissions.add(Permission.objects.get(name='can answer tickets'))
                login(request, user)
                return HttpResponseRedirect('/dashboard')
            else:
                messages.error(request, 'Invalid password!')
        form = AgentForm()
        kind = 1
        return render(request, 'login_user.html', {'form': form, 'kind':kind})
    
    def register(request):
        if request.method == 'POST':
            form = UserForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.user_permissions.add(Permission.objects.get(name='can create tickets'))
                user.user_permissions.add(Permission.objects.get(name='can change tickets'))
                login(request, user)
                return HttpResponseRedirect('/dashboard')
            else:
                messages.error(request, 'Invalid password!')
        form = UserForm()
        kind = 2
        return render(request, 'login_user.html', {'form': form, 'kind':kind})
    
    def logout_user(request):
        logout(request)
        return HttpResponseRedirect('/')
    
    def log_in(request):
        if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid:
                username = form.data['username']
                password = form.data['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect('/dashboard')
                else:
                    messages.error(request, 'Wrong username or password!')
        form = AuthenticationForm()
        kind = 3
        return render(request, 'login_user.html', {'form': form, 'kind':kind})

    def dashboard(request):
        tickets = None
        if request.user.has_perm('main.create_tickets'):
            tickets = TicketModel.objects.all().filter(author=request.user).exclude(status='C')
        if request.user.has_perm('main.answer_tickets'):
            tickets = TicketModel.objects.all().exclude(status='C')
        if tickets is not None:
            info = [tickets.count(), tickets.filter(priority='1').count(), tickets.filter(priority='2').count(), tickets.filter(priority='3').count(), tickets.filter(priority='4').count()]
            return render(request, 'dashboard.html', {'info':info, 'tickets':tickets})
        return render(request, 'dashboard.html')

    def about_us(request):
        return render(request, 'about_us.html')
    
    def profile(request):
        if request.method == 'POST':
            if len(request.POST.get('change-username')) > 0:
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
                else:
                    curr = form.save(commit=False)
                    curr.author = request.user
                    if request.FILES.get('file-name') is not None:
                        curr.file = request.FILES.get('file-name')
                    curr.save()
                    return HttpResponseRedirect('/tickets')
        return render(request, 'send_ticket.html', {'form':form})
    
    @permission_required('main.rewrite_tickets', raise_exception=True)
    def get_tickets(request):
        tickets = TicketModel.objects.all().filter(author=request.user).order_by('priority')
        comments = CommentTicketModel.objects.all()
        more = [[comment for comment in comments.all().filter(ticket=ticket)] for ticket in tickets.all()]
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
            comment = CommentTicketModel.objects.create(ticket=ticket, text=request.POST.get('more-info'), number=ticket.ticket_comments)
            comment.save()
            ticket.save()
        if request.POST.get('file-button-name') is not None:
            id = int(request.POST.get('file-button-name'))
            ticket = tickets.get(id=id)
            filepath = str(ticket.file)
            return FileResponse(open(filepath, 'rb'))
        return render(request, 'tickets.html', {'tickets':tickets, 'comments':comments, 'more':more})
    
    @permission_required('main.rewrite_tickets', raise_exception=True)
    def rewrite(request, id):
        ticket = TicketModel.objects.get(pk=id)
        form = TicketModelForm(request.POST or None, instance=ticket)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/tickets')
        return render(request, 'send_ticket.html', {'ticket':ticket, 'form':form})
    
    @permission_required('main.rewrite_tickets', raise_exception=True)
    def view_answers(request, id):
        ticket = TicketModel.objects.get(pk=id)
        answers = AnswerModel.objects.all().filter(ticket=ticket)
        comments = CommentAnswerModel.objects.all()
        if request.POST.get('comment') is not None:
            id = int(request.POST.get('comment'))
            answer = answers.get(id=id)
            answer.answer_comments += 1
            comment = CommentAnswerModel.objects.create(answer=answer, text=request.POST.get('more-info'), number=answer.answer_comments)
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
            send_erasing_email(ticket.title, ticket.text, request.POST.get('because'), request.user.username, ticket.author.email)
            ticket.delete()
        if request.POST.get('file-button-name') is not None:
            id = int(request.POST.get('file-button-name'))
            ticket = tickets.get(id=id)
            filepath = str(ticket.file)
            return FileResponse(open(filepath, 'rb'))
        return render(request, 'tickets.html', {'tickets':tickets, 'comments':comments})
    
    @permission_required('main.answer_tickets', raise_exception=True)
    def answer(request, id):
        ticket = TicketModel.objects.get(pk=id)
        answers = AnswerModel.objects.all().filter(ticket=ticket).order_by('number')
        form = AnswerModelForm(request.POST)
        comments = CommentAnswerModel.objects.all().order_by('answer')
        if request.method == 'POST':
            if request.POST.get('comment') is not None:
                id = int(request.POST.get('comment'))
                answer = answers.get(pk=id)
                answer.answer_comments += 1
                comment = CommentAnswerModel.objects.create(answer=answer, text=request.POST.get('more-info'), number=answer.answer_comments)
                answer.save()
                comment.save()
                return HttpResponseRedirect('/answer/{}'.format(ticket.id))
            if request.POST.get('close_ticket') is not None:
                id = int(request.POST.get('close_ticket'))
                ticket = TicketModel.objects.get(pk=id)
                ticket.status = 'C'
                ticket.save()
                return HttpResponseRedirect('/list_tickets')
            if form.is_valid():
                if len(form.data.get('text')) == 0:
                    messages.error(request, 'Empty answer!')
                else:
                    curr = form.save(commit=False)
                    curr.ticket = ticket
                    ticket.num_answers += 1
                    ticket.status = 'O'
                    curr.number = ticket.num_answers
                    curr.save()
                    ticket.save()
                    if request.POST.get('send_to_mail') == 'yes':
                        send_answering_email(ticket.title, ticket.text, curr.text, request.user.username, ticket.author.email)
                    return HttpResponseRedirect('/list_tickets')
        return render(request, 'answer.html', {'ticket':ticket, 'form':form, 'answers':answers, 'comments':comments})
    
    @permission_required('main.answer_tickets', raise_exception=True)
    def knowledge_base(request):
        tickets = TicketModel.objects.all().filter(status='C')
        comments = CommentTicketModel.objects.all()
        paginator = Paginator(tickets, 3)
        page_number = request.GET.get('page')
        object = paginator.get_page(page_number)
        return render(request, 'knowledge_base.html', {'tickets':object, 'comments':comments})
