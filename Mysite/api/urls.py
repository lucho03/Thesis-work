from django.urls import path
from .view import answers, tickets, comments_answer, comments_ticket, data

urlpatterns = [
    path('', data, name='api_data'),
    path('tickets', tickets, name='api_tickets'),
    path('answers', answers, name='api_answers'),
    path('comments_answer', comments_answer, name='api_comments_1'),
    path('comments_ticket', comments_ticket, name='api_comments_2')
]