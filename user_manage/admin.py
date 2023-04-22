from django.contrib import admin
from .models import *

# Register your models here.

class UserManageAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username','created','is_active')
admin.site.register(LoginUser, UserManageAdmin)