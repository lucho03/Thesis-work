from django.test import TestCase
from django.contrib.auth.models import User
from .models import TicketModel, AnswerModel

class Test(TestCase):
    def setUp(self):
        self.ticket = TicketModel.objects.create(author=User.objects.create(username='Customer'), text='opa')
        self.answer = AnswerModel.objects.create(author=User.objects.create(username='Employee'), ticket=self.ticket, text='Answer')

    def test_replying(self):
        assert TicketModel.objects.get(pk=1) == AnswerModel.objects.get(pk=1).ticket
    
    def test_author(self):
        assert User.objects.get(pk=1) == TicketModel.objects.get(pk=1).author
        
    def test_auhtor2(self):
        assert User.objects.get(pk=2) == AnswerModel.objects.get(pk=1).author