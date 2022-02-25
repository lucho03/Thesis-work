from django.urls import path
from main.views import Tickets, View

urlpatterns = [
    path('', View.main_page),
    path('dashboard', View.dashboard),
    path('profile', View.profile),
    path('about us', View.about_us),
    path('tickets', Tickets.get_tickets),
    path('send_ticket', Tickets.set_ticket),
    path('rewrite/<id>', Tickets.rewrite, name='rewrite'),
    path('view_answer/<id>', Tickets.view_answers, name='view_answers'),
    path('register', View.register, name='register'),
    path('register_agent', View.register_agent, name='register_agent'),
    path('logout_user', View.logout_user),
    path('log_in', View.log_in),
    path('list_tickets', Tickets.list_tickets),
    path('answer/<id>', Tickets.answer, name='answer')
]