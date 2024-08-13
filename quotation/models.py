from django.db import models
from authAPI.models import User
from productsAPI.models import Product

# Create your models here.
class QuotationHeader(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class QuotationDetail(models.Model):
    quotation_header = models.ForeignKey(QuotationHeader, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    quotation_mensual = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    