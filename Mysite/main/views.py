from django.urls import reverse
from multiprocessing.connection import answer_challenge
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.models import Permission

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, permission_required
from .forms import AnswerModelForm, TicketModelForm, UserForm
from .models import AnswerModel, TicketModel 

from django.contrib import messages

class View(TemplateView):
    def main_page(request):
        return render(request, 'main_page.html')
    '''
    def register_agent(request):
        if request.method == 'POST':
            form = UserForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.user_permissions.add(Permission.objects.get(name='can answer tickets'))
                login(request, user)
                return HttpResponseRedirect('/dashboard')
            else:
                messages.error(request, 'Invalid password!')
        form = UserForm()
        return render(request, 'login_user.html', {'form': form})
    '''
    def register(request):
        if request.method == 'POST':
            form = UserForm(request.POST)
            if form.is_valid():
                user = form.save()
                #user.user_permissions.add(Permission.objects.get(name='can answer tickets'))
                user.user_permissions.add(Permission.objects.get(name='can create tickets'))
                user.user_permissions.add(Permission.objects.get(name='can change tickets'))
                login(request, user)
                return HttpResponseRedirect('/dashboard')
            else:
                messages.error(request, 'Invalid password!')
        form = UserForm()
        return render(request, 'login_user.html', {'form': form})
    
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
        return render(request, 'login_user.html', {'form': form})
    
    def dashboard(request):
        tickets = None
        if request.user.has_perm('main.create_tickets'):
            tickets = TicketModel.objects.all().filter(author=request.user)
        if request.user.has_perm('main.answer_tickets'):
            tickets = TicketModel.objects.all()
        if tickets is not None:
            info = [tickets.count(), tickets.filter(priority='1').count(), tickets.filter(priority='2').count(), tickets.filter(priority='3').count(), tickets.filter(priority='4').count()]
            return render(request, 'dashboard.html', {'info':info})
        return render(request, 'dashboard.html')

    def about_us(request):
        return render(request, 'about_us.html')


class Tickets(TemplateView):
    @login_required(login_url='/log_in')
    @permission_required('main.create_tickets', raise_exception=True)
    def set_ticket(request):
        form = TicketModelForm(request.POST)
        if request.method == 'POST':    
            if form.is_valid():
                if len(form.data.get('text')) == 0:
                    messages.error(request, 'Empty ticket!')
                else:
                    curr = form.save(commit=False)
                    curr.author = request.user
                    curr.save()
                return HttpResponseRedirect('/tickets')
            
        return render(request, 'send_ticket.html', {'form':form})
    
    @login_required(login_url='/log_in')
    @permission_required('main.rewrite_tickets', raise_exception=True)
    def get_tickets(request):
        tickets = TicketModel.objects.all().filter(author=request.user).order_by('priority')
        id = None
        if request.POST.get('change') is not None:
            id = int(request.POST.get('change'))
        if id is not None:
            return HttpResponseRedirect(reverse('rewrite', kwargs={'id':id}))
        return render(request, 'tickets.html', {'tickets':tickets})
    
    @login_required(login_url='/log_in')
    @permission_required('main.rewrite_tickets', raise_exception=True)
    def rewrite(request, id):
        ticket = TicketModel.objects.get(pk=id)
        form = TicketModelForm(request.POST or None, instance=ticket)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/tickets')
        return render(request, 'send_ticket.html', {'ticket':ticket, 'form':form})
    
    @login_required(login_url='/log_in')
    @permission_required('main.answer_tickets', raise_exception=True)
    def list_tickets(request):
        tickets = TicketModel.objects.all().order_by('priority')
        id = None
        if request.POST.get('answer') is not None:
            id = int(request.POST.get('answer'))
        if id is not None:
            return HttpResponseRedirect(reverse('answer', kwargs={'id':id}))
        return render(request, 'tickets.html', {'tickets':tickets})
    
    @login_required(login_url='/log_in')
    @permission_required('main.answer_tickets', raise_exception=True)
    def answer(request, id):
        ticket = TicketModel.objects.get(pk=id)
        answers = AnswerModel.objects.all().filter(ticket=ticket)
        form = AnswerModelForm(request.POST)
        if request.method == 'POST':    
            if form.is_valid():
                if len(form.data.get('text')) == 0:
                    messages.error(request, 'Empty answer!')
                else:
                    curr = form.save(commit=False)
                    curr.ticket = ticket
                    ticket.num_answers += 1
                    curr.number = ticket.num_answers
                    curr.save()
                    ticket.save()
                    return HttpResponseRedirect('/list_tickets')
        return render(request, 'answer.html', {'ticket':ticket, 'form':form, 'answers':answers})