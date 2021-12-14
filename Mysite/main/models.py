from django.db import models

class TicketModel(models.Model):
    author = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return 'Author : ' + self.author + ' Email: ' + self.email + ' Text: ' + self.text