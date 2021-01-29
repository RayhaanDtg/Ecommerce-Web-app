from django.shortcuts import render
from django.shortcuts import render, redirect
from BillingProfile.models import BillingProfile
from Order.models import Order
from account.forms import Login_Form, Guest_Form
from account.models import GuestEmail
from addresses.forms import AddressForm
from .models import Address
from django.utils.http import is_safe_url


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
