from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

class TicketModel(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    text = models.TextField()
    #date = models.DateTimeField(default=now, blank=True)