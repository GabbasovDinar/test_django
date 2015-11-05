from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import *
 
class PoductInLine(admin.TabularInline):
    model = Product
    extra = 3   
    
class OrderProductLineInLine(admin.TabularInline):
    model = OrderProductLine
    extra = 3    
    
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'

class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )

class ProductCategoryAdmin(admin.ModelAdmin):
    fields = ['NameCategory']
    inlines = [PoductInLine]
    search_fields = ['NameCategory']

class DeliveryServiceAdmin(admin.ModelAdmin):
    fields = ['NameServis', 'Telephone']
    list_display = ('NameServis', 'Telephone')
    search_fields = ['NameServis']
  
class OrderAdmin(admin.ModelAdmin):
    fields = ['UserID', 'DateOrder']
    inlines = [OrderProductLineInLine]
    list_display = ('UserID', 'DateOrder')
    search_fields = ['UserID']    
    list_filter = ['DateOrder']

class CashMoveAdmin(admin.ModelAdmin):
    fields = ['UserCash', 'DateCashMove', 'AmountMoney']
    list_display = ('UserCash', 'DateCashMove')
    search_fields = ['UserCash']    
    list_filter = ['DateCashMove']    
    
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(CashMove, CashMoveAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(DeliveryService, DeliveryServiceAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProductLine)