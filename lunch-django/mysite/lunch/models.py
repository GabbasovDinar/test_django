from django.db import models
import datetime
from django.utils import timezone

class User(models.Model):
    NameUser = models.CharField(max_length=100)
    SurnameUser = models.CharField(max_length=100)
    Login = models.CharField(max_length=100)
    Email = models.EmailField(max_length=100)
    Password = models.CharField(max_length=100)
    RegistrationDate = models.DateTimeField('registration date')
    Authority = models.CharField(max_length=10)
    Balance = models.FloatField()
    RegistrationCheck = models.BooleanField()
    def __str__(self): 
        return self.NameUser
    
    
class CashMove(models.Model):
    AmountMoney = models.FloatField()
    DateCashMove = models.DateTimeField('date')
    UserCash = models.ForeignKey('User')
    def __str__(self): 
        return str(self.AmountMoney) 
    
    
class Product(models.Model):
    NameProduct = models.CharField(max_length=30)
    Price = models.FloatField()
    DeliveryID = models.ForeignKey('DeliveryService')
    ProductCategoryID = models.ForeignKey('ProductCategory')
    def __str__(self): 
        return self.NameProduct      
    
class ProductCategory(models.Model):
    NameCategory = models.CharField(max_length=30)
    def __str__(self): 
        return self.NameCategory   
    
class Order(models.Model):
    DateOrder = models.DateTimeField('date order product')
    UserID = models.ForeignKey('User')
    def __str__(self): 
        return str(self.UserID)
    
class OrderProductLine(models.Model):
    NumProduct = models.IntegerField()
    Confirmation = models.BooleanField()
    OrderID = models.ForeignKey('Order')
    ProductID = models.ForeignKey('Product')
    def __str__(self): 
        return str(self.NumProduct)
        
class DeliveryService(models.Model):
    NameServis = models.CharField(max_length=30)
    Telephone = models.CharField(max_length=30)
    def __str__(self): 
        return self.NameServis 