from django.db import models
from uuid import uuid4 

import json

class Login(models.Model):
    user_id = models.AutoField(primary_key=True)
    email_address = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return str(self.user_id)

class User(models.Model):
    user_id = models.ForeignKey('Login', on_delete=models.CASCADE)
    email_address = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.user_id)

class Company(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    # company_address = models.CharField(max_length=255)
    # company_city = models.CharField(max_length=255)
    # company_zip = models.CharField(max_length=255)
    # company_phone = models.CharField(max_length=255)
    # company_email = models.CharField(max_length=255)
    company_id = models.UUIDField(default=uuid4, editable=False, unique=True)

    def __str__(self):
        return str(self.user_id)

class Account(models.Model):
    company_id = models.ForeignKey('Company', on_delete=models.CASCADE)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.company_id)

class Product(models.Model):
    company_id = models.ForeignKey('Account', on_delete=models.CASCADE)
    url = models.CharField(max_length=255)
    ebay_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    wholesale_price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    retail_price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    profit = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    profit_percentage = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    wholesale_weight = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    wholesale_fee = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    units_sold = models.IntegerField()
    updates = models.CharField(max_length=255, blank=True)
    date = models.DateTimeField(auto_now=True)
    image = models.CharField(max_length=255)
    source = models.CharField(max_length=255)

    def __str__(self):
        return str(self.company_id)

class Projection(models.Model):
    company_id = models.ForeignKey('Product', on_delete=models.CASCADE)
    purchase_name = models.CharField(max_length=255)
    purchase_price = models.CharField(max_length=255)
    purchase_quantity = models.IntegerField()
    purchase_date = models.CharField(max_length=255)

    def __str__(self):
        return str(self.company_id)