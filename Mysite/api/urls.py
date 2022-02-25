from django.urls import path
from .view import answers, tickets, data

urlpatterns = [
    path('', data, name='api_data'),
    path('tickets', tickets, name='api_tickets'),
    path('answers', answers, name='api_answers')
]