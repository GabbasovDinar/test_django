from django.contrib import admin
from .models import *

class CashMoveInLine(admin.TabularInline):
    model = CashMove
    extra = 1    
class PoductInLine(admin.TabularInline):
    model = Product
    extra = 3   
class OrderProductLineInLine(admin.TabularInline):
    model = OrderProductLine
    extra = 3    
    
class UserAdmin(admin.ModelAdmin):
    fieldsets = [
            (None,               {'fields': ['Login', 'Password', 'RegistrationCheck']}),
            ('Registration', {'fields': ['NameUser', 'SurnameUser', 'Email', 'RegistrationDate', 'Authority', 'Balance'], 'classes': ['collapse']}),
    ]
    inlines = [CashMoveInLine]
    list_display = ('Login', 'NameUser', 'RegistrationDate')
    list_filter = ['RegistrationDate']
    search_fields = ['Login']
    
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
   
admin.site.register(User, UserAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(DeliveryService, DeliveryServiceAdmin)
admin.site.register(Order, OrderAdmin)