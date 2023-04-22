from django.db import models

# Create your models here.


class FileManager(models.Model):
    user_code = models.CharField(max_length=50, blank=False, null=True)
    upload = models.FileField(upload_to ='file_manager')
    is_active = models.BooleanField(default=True)
    expiry_date = models.IntegerField(default=0)