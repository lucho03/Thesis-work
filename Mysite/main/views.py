from django.shortcuts import render
from django.views.generic.base import TemplateView

class View(TemplateView):
    def dashboard(request):
        return render(request, 'dashboard.html')

    def about_us(request):
        return render(request, 'about_us.html')