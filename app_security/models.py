from django.db import models
from django.utils import timezone

# Create your models here.

class SecurityKey(models.Model):
    user_value 		= models.CharField(max_length=200)
    key 			= models.CharField(max_length=200)
    is_active 	    = models.BooleanField(default=True, null=True)
    is_onetime 	    = models.BooleanField(default=True, null=True)
    created		 	= models.DateTimeField(default=timezone.now)
    
    def save(self, *args, **kwargs):
        import random
        r1 = random.randint(9999, 99999)
        self.key = self.encrypt(r1)
        super(SecurityKey, self).save(*args, **kwargs)
        
    def encrypt(text):
        from cryptography.fernet import Fernet
        key = Fernet.generate_key()
        f = Fernet(key)
        encrypted_data = f.encrypt(text)
        return encrypted_data