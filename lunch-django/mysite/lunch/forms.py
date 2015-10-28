from django import forms
from .models import *

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('NameUser', 'SurnameUser', 'Login', 'Email', 'Password', 'Authority', 'Balance', 'RegistrationCheck')