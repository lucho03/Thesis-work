import email
import os
from django.contrib.auth.models import User
from django.db import models
from pyparsing import empty

class TicketModel(models.Model):
    PRIORITIES = (
        ('1', 'Urgent'),
        ('2', 'High'),
        ('3', 'Medium'),
        ('4', 'Low')
    )
    TYPES = (
        ('Q', 'Question'),
        ('P', 'Problem'),
        ('I', 'Incident'),
        ('R', 'Request'),
        ('O', 'Order')
    )
    STATUSES = (
        ('N', 'New'),
        ('O', 'Open'),
        ('P', 'Pending'),
        ('R', 'Resolved'),
        ('C', 'Closed')
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(default='Title')
    text = models.TextField()
    ticket_comments = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(max_length=1, choices=PRIORITIES, default='3')
    type = models.CharField(max_length=1, choices=TYPES, default='Q')
    status = models.CharField(max_length=1, choices=STATUSES, default='N')
    num_answers = models.IntegerField(default=0)
    file = models.FileField(null=True)

    def filename(self):
        return os.path.basename(self.file.name)
    
    def delete(self, using=None, keep_parents=False):
        storage = self.file.storage
        if len(self.file.name) > 0:
            if storage.exists(self.file.name):
                storage.delete(self.file.name)
        super().delete()

    class Meta:
        permissions = (
            ('create_tickets', 'can create tickets'),
            ('rewrite_tickets', 'can change tickets'),
            ('answer_tickets', 'can answer tickets')
        )

class AnswerModel(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    ticket = models.ForeignKey(TicketModel, on_delete=models.CASCADE)
    text = models.TextField()
    answer_comments = models.IntegerField(default=0)
    number = models.IntegerField(default=0)
    lock = models.BooleanField(default=False)

class CommentTicketModel(models.Model):
    ticket = models.ForeignKey(TicketModel, on_delete=models.CASCADE)
    text = models.TextField(default='T')
    number = models.IntegerField(default=0)

class CommentAnswerModel(models.Model):
    answer = models.ForeignKey(AnswerModel, on_delete=models.CASCADE)
    text = models.TextField(default='T')
    number = models.IntegerField(default=0)

class RegisterAgent(models.Model):
    email = models.EmailField(default='example@gmail.com')