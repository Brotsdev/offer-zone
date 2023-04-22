from django.contrib import admin
from .models import *

# Register your models here.

class UserAuthKeyAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'code')
admin.site.register(UserAuthKey, UserAuthKeyAdmin)