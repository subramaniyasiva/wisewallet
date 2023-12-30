# wisewallet/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from expense.models import WExpense 

class CustomUserAdmin(UserAdmin):
    # Define your custom user admin settings here
    pass

admin.site.register(CustomUser, CustomUserAdmin)
