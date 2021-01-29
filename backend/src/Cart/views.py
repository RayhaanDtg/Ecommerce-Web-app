from django.http import Http404
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Cart, CartManager
from BillingProfile.models import BillingProfile
from Order.models import Order
from account.forms import Login_Form, Guest_Form
from account.models import GuestEmail
from addresses.forms import AddressForm
from addresses.models import Address


def cart_view(request):
    cart_obj, new_obj = Cart.objects.new_or_create(request)
    context = {
        "cart": cart_obj
    }
    return render(request, 'carts/cart_view.html', context)


def cart_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_create(request)
    product_list = []
    for x in cart_obj.products.all():
        product_list.append(
            {
                "id": x.id,
                "name": x.name,
                "price": x.price,
                "url": x.get_absolute_url()
            }
        )
    json_data = {
        "products": product_list,
        "total": cart_obj.total
    }
    return JsonResponse(json_data)


# function in view that is called when update cart url is requested.
# gets the product ID of the request
# if product is in the cart, remove it, else add it.
# after the function is executed, redirects to the cart page
def cart_update(request):
    print(request.POST)
    success, count = Cart.objects.update_cart(request)
    request.session['cart_items'] = count
    if request.is_ajax():
        print("request was ajax")
        print(success)
        print(count)
        json_data = {
            "added": success,
            "removed": not success,
            "items": count
        }
        return JsonResponse(json_data)
    return redirect("Cart:CartHome")


# creates an order for the checkout and set the billing profile and cart to the order
# enables to either login to check out or continue as guest
# if guest, retrieved guest id. creates the billing profile according to whether user logged in or is guest
# if billing profile was created successfully, create the order and associate it with billing and cart
def checkout(request):
    cart_obj, cart_created = Cart.objects.new_or_create(request)

    if cart_created or cart_obj.products.count() == 0:
        return redirect("Cart:CartHome")
    login_form = Login_Form()
    guest_form = Guest_Form()
    address_form = AddressForm()
    address_id = request.session.get('address_id')

    billing_obj, billing_bool = BillingProfile.objects.new_or_get(request=request)
    qs = Address.objects.filter(billing_profile=billing_obj)
    order_obj = Order.objects.finalize_check(request=request, billing_profile=billing_obj, address_id=address_id,
                                             cart_obj=cart_obj)

    if request.method == 'POST':
        result = order_obj.check_success()
        if result:
            order_obj.mark_paid()
            del request.session['cart_id']
            return redirect("Cart:CartSuccess")

    context = {
        "order": order_obj,
        "form": login_form,
        "billing": billing_obj,
        "guest": guest_form,
        "address": address_form,
        "qs": qs
    }

    return render(request, 'carts/checkout.html', context)
