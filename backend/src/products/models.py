import os
import random
from django.db.models import Q, signals
from django.dispatch import receiver
from rest_framework import serializers
from .utilities import unique_slug_generator
from django.db.models.signals import pre_save, post_save
from django.db import models
from django.urls import reverse


# creating a product model and making the fields with all necessities such as
# length of fields, default and so on
# also include the model file in my installed app in settings
# always when changing model class do makemigrations and migrate


# this function gets the full basename (directory) of a filename. Then splits the filename into only the name of file
# and extension
def get_filename(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


# gives the file to upload with a specific random integer as filename with extension
# then uploads it to a specific url in the db
def upload_img(instance, filepath):
    new_filename = random.randint(0, 10000)
    name, ext = get_filename(filepath)
    final = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "products/{new_filename}{final}".format(new_filename=new_filename, final=final)


# defines a class that inherits from the QuerySet class. It is a class applied to manager objects to perform queries.
# Define your own query methods here that return a query set. Uses self which means using a QuerySet object to (since
# it inherits from QuerySet class). These methods are then applied to the get_queryset method to execute. Enabling
# chaining of query methods modify queries
class ProductQuerySet(models.QuerySet):
    def in_stock(self):
        qs = self.filter(InStock=True)
        return qs

    def searched(self, query):
        lookups = Q(title__icontains=query) | Q(
            description__icontains=query) | Q(price__icontains=query)
        print(lookups)
        qs = self.filter(lookups)
        print(qs.query)
        return qs


# customised Manager Object to manipulate objects in database. Has it's own get_queryset method that inherits from
# customized QuerySet class.
class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, self._db)

    def get_in_stock(self):
        qs = self.get_queryset().in_stock()
        return qs

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            instance = qs.first()
            return instance
        else:
            return None

    def get_search(self, query):
        qs = self.get_queryset().searched(query)
        print(qs.query)
        return qs




# the product model with all the fields to be included


class Product(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=20, default=0.00, decimal_places=2)
    image = models.ImageField(upload_to=upload_img, null=True, blank=True)
    objects = ProductManager()
    InStock = models.BooleanField(default=False)

    # represents the model object in the db with the name instead of Product Object
    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    @property
    def name(self):
        return self.title

    # returns the absolute url of an instance of a product
    def get_absolute_url(self):
        # return "/products/{slug}/".format(slug=self.slug)
        return reverse("products:ProductDetail", kwargs={"slug": self.slug})


# function that gives a product a randomly generated slug  before it is saved in the db
# this function is called by pre_save.connect


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    print('pre save slug')
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
        instance.save()

        print(instance.slug)


pre_save.connect(product_pre_save_receiver, sender=Product)
