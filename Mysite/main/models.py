from django.db import models

class Ticket(models.Model):
    author = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)