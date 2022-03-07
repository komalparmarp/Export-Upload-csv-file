from django.db import models


# Create your models here.
class Product(models.Model):
    p_name = models.CharField(max_length=20, blank=True, null=True)
    price = models.PositiveIntegerField(blank=True, null=True)
