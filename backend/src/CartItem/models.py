from django.db import models
from django.conf import settings
from products.models import Product
from django.db.models.signals import m2m_changed
from rest_framework import serializers
from products.models import Product
# from Cart.models import Cart


class CartItemManager(models.Manager):
       
    def retrieve_or_create(self,cart,product):
        cart_qs=self.get_queryset().filter(cart=cart,isActive=True)
        if cart_qs.count()!=0:
            cart_item_list=cart_qs.filter(product=product,isActive=True)
            if cart_item_list.count()!=0:
                cart_item=cart_item_list.first()
            else:
                cart_item=self.create(product=product,cart=cart,isActive=True)
        else:
            cart_item=self.create(product=product,cart=cart,isActive=True)
        return cart_item

    def get_list_cart_items(self,cart):
        qs= self.get_queryset().filter(cart=cart,isActive=True)
        return qs

    def get_by_id(self,id):
        qs= self.get_queryset().filter(id=id,isActive=True)
        return qs
# Create your models here.
class CartItem(models.Model):
    product=models.ForeignKey(Product,blank=True,null=True,on_delete=models.CASCADE)
    cart=models.ForeignKey('Cart.Cart',blank=True,null=True,on_delete=models.CASCADE)
    subtotal= models.DecimalField(default=0.00, max_digits=20, decimal_places=2)
    qty=models.IntegerField(default=0,blank=True,null=True)
    isActive= models.BooleanField(default=False)
    objects=CartItemManager()

    def __str__(self):
        return str(self.product)
    
          

    # @property
    # def qty(self):
    #     return self.qty
    
    # @property
    # def isActive(self):
    #     return self.isActive

    # @property
    # def cart(self):
    #     return self.cart
    
    # @property 
    # def id(self):
    #     return self.id

    # @property
    # def product(self):
    #     return self.product
    
    # @property
    # def subtotal(self):
    #     return self.subtotal
    




        

        

