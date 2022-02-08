from django.contrib.auth.models import User
from django.db import models

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
        ('O', 'Open'),
        ('P', 'Pending'),
        ('R', 'Resolved'),
        ('C', 'Closed')
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(default='Title')
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(max_length=1, choices=PRIORITIES, default='4')
    type = models.CharField(max_length=1, choices=TYPES, default='Q')
    status = models.CharField(max_length=1, choices=STATUSES, default='O')
    num_answers = models.IntegerField(default=0)

    class Meta:
        permissions = (
            ('create_tickets', 'can create tickets'),
            ('rewrite_tickets', 'can change tickets'),
            ('answer_tickets', 'can answer tickets')
        )

class AnswerModel(models.Model):
    ticket = models.ForeignKey(TicketModel, on_delete=models.CASCADE)
    text = models.TextField()
    number = models.IntegerField(default=0)