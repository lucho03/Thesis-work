import email
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

class TicketModel(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(default=now, blank=True)

    class Meta:
        permissions = (
            ('answer_tickets', 'can answer tickets'),
        )