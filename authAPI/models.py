from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    photo = models.ImageField(default='usuario.png', upload_to='media')
    phone = models.CharField(max_length=10, null=True)
    identity = models.CharField(max_length=10, null=True)
    is_verified = models.BooleanField(default=False)