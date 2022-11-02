from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,PermissionsMixin,Group
)
import os
from django.conf import settings
from django.utils import timezone
# from phonenumber_field.modelfields import PhoneNumberField
# from django.contrib.postgres.fields import JSONField
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email,username, password=None, **extra_fields):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username = username,
            **extra_fields
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user


    # def create_superuser(self, email,username, date_of_birth, password, **extra_fields):
    def create_superuser(self, email,username, password, **extra_fields):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email = email,
            username = username,
            password=password,
        )
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)


        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})


class LoginUser(AbstractBaseUser,PermissionsMixin):
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

    objects = UserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number']

    def __str__(self):
        return self.username