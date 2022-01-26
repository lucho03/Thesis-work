from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now, localtime
import datetime

class TicketModel(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = (
            ('create_tickets', 'can create tickets'),
            ('rewrite_tickets', 'can change tickets'),
            ('answer_tickets', 'can answer tickets')
        )