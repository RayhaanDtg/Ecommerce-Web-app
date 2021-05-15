from django.db import models
from django.conf import settings
from products.models import Product
from django.db.models.signals import m2m_changed
from rest_framework import serializers
from CartItem.models import CartItem
from stock.models import Stock
import decimal

# from account.models import User

User = settings.AUTH_USER_MODEL


# creates a custom Manager object

class CartManager(models.Manager):


    def retrieve_or_create(self,user):
        qs=self.get_queryset().filter(user=user,isActive=True)
        if qs.count() == 1:
            cart_obj=qs.first()
        else:
            cart_obj=self.model.objects.create(user=user)
            cart_obj.isActive=True
            cart_obj.save()
        return cart_obj

    # checks if a cart already exists by getting the cart id of the session
    # retrieves the carts based on the id
    # if there is a user which is authenticated and the user associated to the cart is None,
    # save the user authenticated in the request to the cart
    # else if there are no carts, create one and associate it with the user in the request
    # save the session ID as the card id
    def new_or_create(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                print(request.user.is_authenticated)
                print('Cart exists already')
                cart_obj.user = request.user
                cart_obj.save()
        else:
            print('New cart')
            cart_obj = self.new_cart(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj

    # new_cart creates a new cart. If there is no authenticated user, it creates a cart
    # without any user. Else, if there is a user, it creates a cart with the authenticated user
    def new_cart(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)

    
    # gets the cart for a specific user.
    # creates or updates a cart_item for a specific cart
    # also updates the total of the cart

    def update_cart_1(self,product,user,qty,price):
        cart_obj=Cart.objects.retrieve_or_create(user=user)
        cart_item=CartItem.objects.retrieve_or_create(cart=cart_obj,product=product)
        cart_item.qty=qty
        cart_item.subtotal=price*decimal.Decimal(qty)
        cart_item.save()
        qs_cart_items=CartItem.objects.get_list_cart_items(cart=cart_obj)
        cart_final_obj=self.update_cart_total(cart=cart_obj)
        return cart_final_obj
    
    def update_cart_total(self,cart):
        qs_cart_items=CartItem.objects.get_list_cart_items(cart=cart)
        cart.total=0
        for x in qs_cart_items:
            cart.total= decimal.Decimal(cart.total)+ x.subtotal
        cart.save()
        return cart

    


    
    



   

    # # function in view that is called when update cart url is requested.
    # # gets the product ID of the request
    # # if product is in the cart, remove it, else add it.
    # # after the function is executed, redirects to the cart page
    # def update_cart(self, request):
    #     added = False
    #     count = 0
    #     product_id = request.POST.get("product_id")

    #     if product_id is not None:
    #         try:
    #             product_obj = Product.objects.get(id=product_id)
    #         except Product.DoesNotExist:
    #             print("Product does not exist")
    #             return added

    #         cart_obj, new_obj = self.new_or_create(request)
    #         if product_obj not in cart_obj.products.all():
    #             cart_obj.products.add(product_obj)
    #             count = cart_obj.products.count()

    #             added = True

    #         else:
    #             cart_obj.products.remove(product_obj)
    #             count = cart_obj.products.count()
    #             added = False

    #         return added, count



class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    # products = models.ManyToManyField(CartItem, blank=True)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    isActive=models.BooleanField(default=False)
    objects = CartManager()

    def __str__(self):
        return str(self.id)

   




# function that is taken as argument in the m2m_changed.connect
# everytime many to many relationship is changed (many products in carts) is changed
# and action is taken, the function takes the sender as the products in the cart
# based on the changes, it then updates the total of the cart
# def update_total(sender, instance, action, *args, **kwargs):
#     if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
#         products = instance.products.all()
#         total = 0
#         for p in products:
#             total = total + (p.sub * p.qty)
#         instance.total = total
#         instance.save()


# m2m_changed.connect(update_total, sender=Cart.products.through)
