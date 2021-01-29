from django.contrib import admin
from .models import Product

# Register your models here. Enables a model to be created in the admin database to be modified

admin.site.register(Product)
