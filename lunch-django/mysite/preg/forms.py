from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['DateOrder']
         
class ProductForm(forms.ModelForm):
    class Meta:
        model = OrderProductLine
        exclude = ['OrderID']
        
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
    username = forms.CharField(label='Name user', error_messages={'required': 'Enter login'}, max_length=30)
    password1 = forms.CharField(label=u'Password', widget=forms.PasswordInput, error_messages={'required': 'Enter the password'}, min_length=4, max_length=30)
    password2 = forms.CharField(label=u'Repeat password', widget=forms.PasswordInput, error_messages={'required': 'Enter the password again'})

    def clean_pass2(self):
        data = self.cleaned_data
        if (data["password2"]!=data.get("password1", "")):
            raise forms.ValidationError("password no match")
        return data["password2"]

    def clean_username(self):
        data = self.cleaned_data
        try:
            User.objects.get(username = data['username'])
        except User.DoesNotExist:
            return data['username']
        raise forms.ValidationError('This username is already taken.') 


