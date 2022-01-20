from django import forms
from django.forms import Textarea
from .models import TicketModel
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
    
    class Meta:
        model = TicketModel
        fields = ['text']
        widgets = {
            'text': Textarea(
                    {'placeholder':('What do you want to know?')}
                )
        }