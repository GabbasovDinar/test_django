from django.db import models
from django.contrib.auth.models import User, UserManager
from django.db.models.signals import post_save
import datetime
from django.utils import timezone


class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)

    balance = models.IntegerField(default=0)
    def __str__(self):
        return str(self.user.username)
    
class CashMove(models.Model):
    AmountMoney = models.FloatField()
    DateCashMove = models.DateTimeField(default=timezone.now)
    def Cashdate(self):
        self.DateCashMove = timezone.now()
        self.save()     
    UserCash = models.ForeignKey('UserProfile')   
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
    DateOrder = models.DateTimeField(blank=True, null=True)
    UserID = models.ForeignKey('UserProfile')
    def publishdate(self):
        self.DateOrder = timezone.now()
        self.save()    
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

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
post_save.connect(create_user_profile, sender=User)