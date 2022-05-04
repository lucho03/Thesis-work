import os
from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField
from django.utils.html import strip_tags

class TicketModel(models.Model):
    PRIORITIES = (
        ('4', 'Low'),
        ('3', 'Medium'),
        ('2', 'High'),
        ('1', 'Urgent')
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
        ('C', 'Closed')
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(default='Title')
    text = RichTextField(config_name='ticket_ckeditor')
    ticket_comments = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(max_length=1, choices=PRIORITIES, default='3')
    type = models.CharField(max_length=1, choices=TYPES, default='Q')
    status = models.CharField(max_length=1, choices=STATUSES, default='N')
    num_answers = models.IntegerField(default=0)
    file = models.FileField(null=True)

    def filename(self):
        return os.path.basename(self.file.name)

    def is_from_email(self):
        return self.author.username.isdigit()

    def clear_text(self):
        return strip_tags(self.text)

    def author_username(self):
        if self.is_from_email():
            return self.author.email
        else:
            return self.author.username

    def delete(self, using=None, keep_parents=False):
        storage = self.file.storage
        if len(self.file.name) > 0:
            if storage.exists(self.file.name):
                storage.delete(self.file.name)
        if self.is_from_email():
            self.author.delete()
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
    title = models.TextField(default='Title')
    text = RichTextField()
    answer_comments = models.IntegerField(default=0)
    number = models.IntegerField(default=0)
    lock = models.BooleanField(default=False)

    def clear_text(self):
        return strip_tags(self.text)

    def author_username(self):
        return self.author.username

class CommentTicketModel(models.Model):
    ticket = models.ForeignKey(TicketModel, on_delete=models.CASCADE)
    author = models.TextField(default='Commentar')
    text = models.TextField(default='Text')
    number = models.IntegerField(default=0)

class CommentAnswerModel(models.Model):
    answer = models.ForeignKey(AnswerModel, on_delete=models.CASCADE)
    author = models.TextField(default='Commentar')
    text = models.TextField(default='Text')
    number = models.IntegerField(default=0)