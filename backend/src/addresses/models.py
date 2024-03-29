from django.db import models
from BillingProfile.models import BillingProfile
from django_countries.fields import CountryField


class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE, null=True, blank=True)
    address_line_1 = models.CharField(max_length=120)
    address_line_2 = models.CharField(max_length=120)
    phone_number=models.IntegerField(max_length=8,null=True,blank=True)

    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120)
    # zip_code = models.CharField(max_length=120)
    # country = CountryField()

    def __str__(self):
        return self.billing_profile.__str__()


