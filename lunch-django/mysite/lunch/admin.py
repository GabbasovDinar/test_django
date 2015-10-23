from django.contrib import admin
from .models import User, CashMove, ProductCategory

class CashMoveInLine(admin.TabularInline):
    model = CashMove
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

admin.site.register(User, UserAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)