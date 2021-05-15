from django.shortcuts import render
from django.shortcuts import render, redirect
from BillingProfile.models import BillingProfile
from Order.models import Order
from account.forms import Login_Form, Guest_Form
from rest_framework.decorators import api_view,permission_classes
from addresses.forms import AddressForm
from .models import Address
from django.utils.http import is_safe_url
from ecom.serializers import AddressSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny
from account.models import User
from rest_framework.response import Response
from django.http import JsonResponse

def checkout_address(request):
    address_form = AddressForm(request.POST or None)
    context = {
        "form": address_form
    }
    next_ = request.GET.get('next')

    next_post = request.POST.get('next')

    redirect_path = next_ or next_post or None
    print("Next for address")
    print(redirect_path)

    if address_form.is_valid():

        instance = address_form.save(commit=False)
        billing_profile, billing_obj = BillingProfile.objects.new_or_get(request)
        if billing_profile is not None:
            instance.billing_profile = billing_profile

            instance.save()
            request.session['address_id'] = instance.id

    else:
        return redirect('Cart:CartCheckout')

    if is_safe_url(redirect_path, request.get_host()):
        if redirect_path is not None:
            print(redirect_path)
            return redirect(redirect_path)

    else:
        return redirect('Cart:CartCheckout')

    return redirect('Cart:CartCheckout')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_address(request):
    email=request.query_params.get('email')
    print("Here is the data for the request for address")
    print(email)
    user=User.objects.filter(email=email)
    if user is not None:
        billing_obj,billing_bool= BillingProfile.objects.get_or_create(user=user.first())
    else:
        billing_obj=None

    address_obj,address_bool=Address.objects.get_or_create(billing_profile=billing_obj)
    print(address_obj)
    address_serializer=AddressSerializer(address_obj)
    json_data={
        "address":address_serializer.data
    }
    print(json_data)
    return JsonResponse(json_data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_data(request):
    message="failed"
    data = request.data
    serialized = AddressSerializer(data=data)
    if serialized.is_valid():
        billing_obj,billing_bool= BillingProfile.objects.get_or_create(id=serialized.data['billing_profile'])
        print(billing_obj)
        address_obj,address_bool=Address.objects.get_or_create(billing_profile=billing_obj)
        address_obj.address_line_1=serialized.data['address_line_1']    
        address_obj.address_line_2=serialized.data['address_line_2'] 
        address_obj.city=serialized.data['city'] 
        address_obj.state=serialized.data['state']
        address_obj.phone_number=serialized.data['phone_number']
        address_obj.save()
        message="success"
    else:
        message="failed"
       
    
    json_data={
        "message":message
    }
    return JsonResponse(json_data)

def reuse_address(request):
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    print("Next for reuse")
    print(redirect_path)
    if request.method == 'POST':
        print(request.POST)
        billing_profile, billing_obj = BillingProfile.objects.new_or_get(request)
        address_id = request.POST.get('Address')
        print("address id for reuse")
        print(address_id)
        if address_id is not None:
            qs = Address.objects.filter(billing_profile=billing_profile, id=address_id)
            if qs.exists() and qs.count() == 1:
                request.session['address_id'] = address_id
            else:
                return redirect('Cart:CartCheckout')
            if is_safe_url(redirect_path, request.get_host()):
                if redirect_path is not None:
                    return redirect(redirect_path)

            else:
                return redirect('Cart:CartCheckout')
    return redirect('Cart:CartCheckout')
