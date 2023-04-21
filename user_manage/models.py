from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,PermissionsMixin,Group
)
import os
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
# from phonenumber_field.modelfields import PhoneNumberField
# from django.contrib.postgres.fields import JSONField
# Create your models here.

class LoginUser(AbstractUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255
    )
    
    username = models.CharField(verbose_name='Username',
        max_length=255,
        unique=True,default='')
    first_name = models.CharField(max_length=255, null=False,default='')
    last_name = models.CharField(max_length=255, null=False,default='')
    country_code = models.CharField(max_length=5, null=True,default='')
    is_staff = models.BooleanField(default=False,null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_shop = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    phone_code = models.CharField(max_length=4, blank=True,null=True)
    phone_number = models.CharField(null=False, blank=False, unique=True,max_length=100)
    created = models.DateTimeField(default=timezone.now)
   
    expiry_date = models.DateField(blank=True, null=True)
    is_eligible = models.SmallIntegerField(default=1,blank = True,null=True)