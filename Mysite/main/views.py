from django import forms
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import TicketModelForm, UserForm
from .models import TicketModel 

from django.contrib import messages

class View(TemplateView):
    def main_page(request):
        return render(request, 'main_page.html')
    
    def register(request):
        if request.method == 'POST':
            form = UserForm(request.POST)
            if form.is_valid():
                user = form.save()
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
                    #print(user.user_permissions.all())
                    return HttpResponseRedirect('/dashboard')
                else:
                    messages.error(request, 'Wrong username or password!')
        
        form = AuthenticationForm()
        return render(request, 'login_user.html', {'form': form})
    
    def dashboard(request):
        return render(request, 'dashboard.html')

    def about_us(request):
        return render(request, 'about_us.html')


class Tickets(TemplateView):
    @login_required(login_url='/log_in')
    def set_ticket(request):
        form = TicketModelForm(request.POST)
        if request.method == 'POST':    
            if form.is_valid():
                curr = form.save(commit=False)
                curr.author = request.user
                curr.save()
                return render(request, 'send_ticket.html', {'form':TicketModelForm(request.GET)})
            
        return render(request, 'send_ticket.html', {'form':form})
    
    @login_required(login_url='/log_in')
    def get_tickets(request):
        tickets = TicketModel.objects.all().filter(author=request.user)
        return render(request, 'tickets.html', {'tickets':tickets})