from django import forms
from .models import *
from django.contrib.auth import authenticate
class OrderForm(forms.ModelForm):
    
    class Meta:
        model = Order
        exclude = ['DateOrder']
class LoginForm(forms.Form):
    username = forms.CharField(label=u'name user')
    password = forms.CharField(label=u'password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        if not self.errors:
            user = authenticate(username=cleaned_data['username'], password=cleaned_data['password'])
            if user is None:
                raise forms.ValidationError(u'name and password no match')
            self.user = user
        return cleaned_data

    def get_user(self):
        return self.user or None
    
    
class RegistrationForm(forms.Form):
    username = forms.CharField(label='Name user', error_messages={'required': 'Enter login'})
    password1 = forms.CharField(label=u'Password', widget=forms.PasswordInput, error_messages={'required': 'Enter the password'})
    password2 = forms.CharField(label=u'Repeat password', widget=forms.PasswordInput, error_messages={'required': 'Enter the password again'})

    def clean_username(self):
        username = self.cleaned_data.get('username')
        return self.cleaned_data

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Pass not match')
        return self.cleaned_data
    
        