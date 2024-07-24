from django.db import models
from authAPI.models import User
from productsAPI.models import Product

# Create your models here.
class Contract(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_start = models.DateField()
    date_end = models.DateField()
    status = models.BooleanField(default=True)
    is_installed = models.BooleanField(default=False)