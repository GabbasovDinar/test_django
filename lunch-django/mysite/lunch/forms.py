from django import forms
from .models import *

class OrderForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ['UserID',]
        
#class OrderLineForm(forms.ModelForm):
    
    #class Meta:
        #model = OrderProductLine
        #fields = ['NumProduct', 'Confirmation', 'OrderID', 'ProductID',]