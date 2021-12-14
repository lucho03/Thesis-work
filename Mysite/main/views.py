from django import forms
from django.shortcuts import render
from django.views.generic.base import TemplateView

from .forms import TicketModelForm
from .models import TicketModel 

class View(TemplateView):
    def main_page(request):
        value = 'HelpDesk System'
        return render(request, 'main_page.html', {'value': value})
    
    def dashboard(request):
        return render(request, 'dashboard.html')

    def about_us(request):
        return render(request, 'about_us.html')


class Tickets(TemplateView):
    def set_ticket(request):
        form = TicketModelForm(request.POST)
        if request.method == 'POST':    
            if form.is_valid():
                form.save()
                return render(request, 'send_ticket.html', {'form':TicketModelForm(request.GET)})
            
        return render(request, 'send_ticket.html', {'form':form})

    def get_tickets(request):
        tickets = TicketModel.objects.all
        return render(request, 'tickets.html', {'tickets':tickets})