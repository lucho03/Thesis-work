from django.shortcuts import render
from django.views.generic.base import TemplateView

class View(TemplateView):
    def main_page(request):
        value = 'HelpDesk System'
        return render(request, 'main_page.html', {'value': value})
    
    def dashboard(request):
        return render(request, 'dashboard.html')

    def about_us(request):
        return render(request, 'about_us.html')


class Tickets(TemplateView):
    def set_ticket():
        pass

    def tickets(request):
        return render(request, 'tickets.html')