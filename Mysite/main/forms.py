from dataclasses import field
from django import forms
from django.forms import Textarea, widgets
from .models import AnswerModel, TicketModel
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def save(self):
        user = super(UserForm, self).save(commit=True)
        return user

class TicketModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TicketModelForm, self).__init__(*args, **kwargs)
        self.fields['text'].required = False
        self.fields['priority'].required = False
        self.fields['type'].required = False
    
    class Meta:
        model = TicketModel
        fields = ['text', 'priority', 'type']
        widgets = {
            'text': Textarea(
                    {'placeholder':('What do you want to know?')}
                )
        }

class AnswerModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AnswerModelForm, self).__init__(*args, **kwargs)
        self.fields['text'].required = False
    
    class Meta:
        model = AnswerModel
        fields = ['text']
        widgets = {
            'text': Textarea()
        }