import math

from django.db import models
from Cart.models import Cart
from BillingProfile.models import BillingProfile
from addresses.models import Address
from django.db.models import signals
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
import datetime

from .utils import unique_order_generator

ORDER_STATUS_CHOICES = (
    ("created", "CREATED"),
    ("paid", "PAID"),
    ("shipped", "SHIPPED"),
    ("refunded", "REFUNDED"),
)


# manager object with new_or_get method.
# This method checks if there is already an order with a specific billing profile and cart and active
# if there is, it returns the order. else it creates a new order obj with the billing profile and cart
class OrderManager(models.Manager):
    def new_or_get(self, billing_profile, cart):
        qs = self.get_queryset().filter(billing_profile=billing_profile, cart=cart, active=True)
        if qs.count() == 1:
            obj = qs.first()
            created = False
        else:
            obj = self.model.objects.create(billing_profile=billing_profile, cart=cart)
            created = True
        return obj, created

    def finalize_check(self, request, billing_profile, address_id, cart_obj):
        order_obj = None
        if billing_profile is not None:
            order_obj, created = self.model.objects.new_or_get(billing_profile=billing_profile, cart=cart_obj)
            if address_id is not None:
                order_obj.address = Address.objects.get(id=address_id)
                del request.session['address_id']
                order_obj.save()

        return order_obj


class Order(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE, null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default="created")
    shipping_total = models.DecimalField(default=10.00, max_digits=100, decimal_places=2)
    order_total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    order_id = models.CharField(max_length=120, blank=True)
    created =  models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    objects = OrderManager()

    def __str__(self):
        return self.order_id

    # updates the total of the order based on the change of the cart items
    def update_total(self):
        cart_total = self.cart.total
        new_total = math.fsum([cart_total, self.shipping_total])
        self.order_total = format(new_total, '.2f')
        self.save()
        return new_total

    # checks if the checkout was successful
    def check_success(self):
        total = self.order_total
        billing = self.billing_profile
        address = self.address
        if billing and address and total > 0:
            return True
        return False

    def mark_paid(self):
        if self.check_success():
            self.status = "paid"
            self.save()
            print(self.status)
        return self.status


# generates an id for the order if the order id does not exists. This executes before order is saved
# checks if an order already exists with the same cart, but not same billing profile.
# if it exists, renders previous orders inactive
def generate_order_id(sender, instance, *args, **kwargs):
    print('Got here for order id')
    if not instance.order_id:
        instance.order_id = unique_order_generator(instance)
    qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)


pre_save.connect(generate_order_id, sender=Order)


# if order is not created, create an order and calculate the total based on the cart it is updated
# sender is the cart
def calc_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()


post_save.connect(calc_cart_total, sender=Cart)


# if order already exists, modify the total based on the changing items in the cart
def calc_order_total(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()


post_save.connect(calc_order_total, sender=Order)
