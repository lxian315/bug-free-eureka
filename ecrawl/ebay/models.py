from django.db import models

import json

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=255)
    ebay_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    wholesale_price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    retail_price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    profit = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    profit_percentage = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    wholesale_weight = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    wholesale_fee = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    units_sold = models.CharField(max_length=255, blank=True)
    updates = models.CharField(max_length=255, blank=True)
    date = models.DateTimeField(auto_now=True)
    image = models.CharField(max_length=255)

    def __str__(self):
        return str(self.id)

class Projection(models.Model):
    id = models.AutoField(primary_key=True)
    purchase_name = models.CharField(max_length=255)
    purchase_price = models.CharField(max_length=255)
    purchase_quantity = models.IntegerField()
    purchase_date = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)