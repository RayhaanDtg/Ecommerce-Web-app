from django.db import models
from django.conf import settings
from products.models import Product
from django.db.models.signals import m2m_changed
from rest_framework import serializers
from CartItem.models import CartItem
from stock.models import Stock
import decimal
from BillingProfile.models import BillingProfile

METHOD_CHOICES=(
(1,"VISA"),
(2,"DEBIT"),
(3,"MASTERCARD")
)

class Payment(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE, null=True, blank=True)
    method=models.CharField(max_length=20, choices=METHOD_CHOICES, default=1)
    card_name=models.CharField(max_length=255,blank=True,null=True)
    card_number=models.DecimalField(default=0, max_digits=100, decimal_places=0)
    expMonth=models.DecimalField(default=0,max_digits=2,decimal_places=0)
    expYear=models.DecimalField(default=0,max_digits=4,decimal_places=0)
    

