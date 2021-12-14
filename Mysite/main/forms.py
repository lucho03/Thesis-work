from django import forms
from django.db.models import fields
from django.forms.widgets import TextInput
from .models import TicketModel

class TicketModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TicketModelForm, self).__init__(*args, **kwargs)
        self.fields['author'].required = False
        self.fields['email'].required = False
        self.fields['text'].required = False
    
    class Meta:
        model = TicketModel
        fields = ['author', 'email', 'text']
        widgets = {
            'author': TextInput({'placeholder':('Name')}),
            'email': TextInput({'placeholder':('Email'), 'value':('email@gmail.com')})
        }