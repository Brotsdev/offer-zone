from django.db import models

# Create your models here.


class MasterCategory(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=250)
    is_admin = models.BooleanField(default=True)