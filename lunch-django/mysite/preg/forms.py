from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import datetime
from django.utils import timezone

#--------------------------Random order---------------------------------

class SimpleForm(forms.Form):
    
    new_choices = []
    new_choices_id = []
    for e in ProductCategory.objects.all():
        new_choices.append(e.NameCategory) 
        new_choices_id.append(e.id)
        
    new_choices = [str(x) for x in new_choices]
    
    new_new = []
    k=0
    for i in new_choices:
        new_new.append((new_choices_id[k], new_choices[k]))
        k=k+1
    THREE_CHOICES = tuple(new_new, )
    Random_order = forms.MultipleChoiceField(choices=THREE_CHOICES, widget=forms.CheckboxSelectMultiple, required=False, error_messages={'required': 'No correct'})

#----------------------------------------------------------------------
        
class OrderConfirmationForm(forms.ModelForm):
    class Meta:
        model = OrderConfirmation
        exclude = ['DateConfirmation', 'ConfirmationOrderID', 'Confirmation', 'OrderProcessing', 'DateProcessing']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['DateOrder', 'UserID']       
        
class ProductForm(forms.ModelForm):
    NumProduct = forms.IntegerField(min_value=1, error_messages={'required': 'Please input num bla bla bla product'})
    #def clean_NumProduct(self): 
        #data = self.cleaned_data        
        #if (data['NumProduct'] == ""):
            #raise forms.ValidationError("Please enter Num product") 
        #return data['NumProduct']      
    class Meta:
        model = OrderProductLine
        exclude = ['Confirmation', 'OrderID', 'NumProduct']


class ConfirmationEditForm(forms.Form):
    Confirmation = forms.BooleanField(False)
        
               
class CashMoveForm(forms.ModelForm):
    class Meta:
        model = CashMove
        exclude='__all__'
        
class ProfilEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
    
class PassEditForm(forms.Form):
    password1 = forms.CharField(label=u'Password', widget=forms.PasswordInput, error_messages={'required': 'Enter the password'}, min_length=4, max_length=30)
    password2 = forms.CharField(label=u'Repeat password', widget=forms.PasswordInput, error_messages={'required': 'Enter the password again'})    
    def clean(self):
        data = self.cleaned_data
        if (data["password2"]!=data.get("password1", "")):
            raise forms.ValidationError("password no match")
        return data 
        
class ConfirmationEditForm(forms.Form):
    Confirmation = forms.BooleanField(False)

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

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        if (cleaned_data["password2"]!=cleaned_data .get("password1", "")):
            raise forms.ValidationError("password no match")
        else:
            try:
                User.objects.get(username = cleaned_data['username'])
            except User.DoesNotExist:
                return cleaned_data
            raise forms.ValidationError('This username is already taken.')
        
class CashUserForm(forms.ModelForm):
    class Meta:
        model = CashMove
        exclude = ['AmountMoney', 'DateCashMove', 'UserCash']