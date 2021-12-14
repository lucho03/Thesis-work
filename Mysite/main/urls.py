from django.contrib import admin
from django.urls import path

from main.views import Tickets, View

urlpatterns = [
    path('', View.main_page),
    path('dashboard', View.dashboard),
    path('about us', View.about_us),
    path('tickets', Tickets.get_tickets),
    path('send_ticket', Tickets.set_ticket)
]