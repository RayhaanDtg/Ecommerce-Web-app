from django.http import Http404
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Cart, CartManager
from BillingProfile.models import BillingProfile
from CartItem.models import CartItem
from Order.models import Order
from account.models import User
from account.forms import Login_Form, Guest_Form
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import api_view,permission_classes
# from account.models import GuestEmail
from addresses.forms import AddressForm
from addresses.models import Address
from ecom.serializers import CartItemSerializer,CartSerializer,ProductSerializer
from products.models import Product
from stock.models import Stock

@api_view(['GET'])
@permission_classes([AllowAny])
def get_cart(request):
    email=request.query_params.get('email')
    print("Here is the data for the request for address")
    print(email)
    user=User.objects.filter(email=email).first()
    print(user)
    cart=Cart.objects.retrieve_or_create(user=user)
    cart_items_list=[]
    product_items_list=[]
    if cart is not None:
        
        qs_cart_items=CartItem.objects.get_list_cart_items(cart=cart)
        if qs_cart_items.count()> 0:
            for x in qs_cart_items:
                # product_item=Product.objects.get_by_id(id=x.product.id)
                # print(x.product.id)
                product_item_serialized=ProductSerializer(x.product)
                product_items_list.append({
                    'product_item':product_item_serialized.data
                })
                cart_item_serialized=CartItemSerializer(x)
                cart_items_list.append({
                    'cart_item': cart_item_serialized.data
                })

    cart_serializer=CartSerializer(cart)
    json_data={
        "cart": cart_serializer.data,
        "cart_items_list":cart_items_list,
        "product_items_list":product_items_list,
    }
    return JsonResponse(json_data)


@api_view(['POST'])
@permission_classes([AllowAny])
def modify_cart(request):
    print(request.data)
    email=request.data['email']
    print(email)
    qty=request.data['qty']
    print(qty)
    product_slug=request.data['slug']
    print(product_slug)
   
    
    print("got here for modifying the cart")
    product=Product.objects.get_by_slug(slug=product_slug)
    print("the product is")
    print(product)
    stock=Stock.objects.get_by_product(product=product)    
    user=User.objects.filter(email=email).first()
    print("price is here")
    print(stock)
    cart_obj=Cart.objects.update_cart_1(product=product,user=user,qty=qty,price=stock.price)
    cart_items_list=[]
    product_items_list=[]
    qs_cart_items=CartItem.objects.get_list_cart_items(cart=cart_obj)
    if qs_cart_items.count()> 0:
        for x in qs_cart_items:
            # product_item=Product.objects.get_by_id(id=x.product.id)
            # print(x.product.id)
            product_item_serialized=ProductSerializer(x.product)
            product_items_list.append({
                'product_item':product_item_serialized.data

                })
            cart_item_serialized=CartItemSerializer(x)
            cart_items_list.append({
                'cart_item': cart_item_serialized.data
            })

    cart_serialized=CartSerializer(cart_obj)
    json_data={
        "cart":cart_serialized.data,
        "cart_items_list":cart_items_list,
        "product_items_list":product_items_list,

    }

    return JsonResponse(json_data)
        




@api_view(['POST'])
@permission_classes([AllowAny])
def delete_from_cart(request):
    print(request.data)
    cart_id=request.data['cart']
    item_id=request.data['cart_item']
    item_obj=CartItem.objects.get_by_id(item_id)
    item_obj.delete()
    cart_obj=Cart.objects.filter(id=cart_id,isActive=True).first()
    final_cart=Cart.objects.update_cart_total(cart=cart_obj)
    cart_items_list=[]
    product_items_list=[]
    qs_cart_items=CartItem.objects.get_list_cart_items(cart=final_cart)
    if qs_cart_items.count()> 0:
        for x in qs_cart_items:
            # product_item=Product.objects.get_by_id(id=x.product.id)
            # print(x.product.id)
            product_item_serialized=ProductSerializer(x.product)
            product_items_list.append({
                'product_item':product_item_serialized.data

                })
            cart_item_serialized=CartItemSerializer(x)
            cart_items_list.append({
                'cart_item': cart_item_serialized.data
            })

    cart_serialized=CartSerializer(final_cart)
    json_data={
        "cart":cart_serialized.data,
        "cart_items_list":cart_items_list,
        "product_items_list":product_items_list,

    }
    return JsonResponse(json_data)





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
    # guest_form = Guest_Form()
    # address_form = AddressForm()
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
        # "guest": guest_form,
        # "address": address_form,
        "qs": qs
    }

    return render(request, 'carts/checkout.html', context)
