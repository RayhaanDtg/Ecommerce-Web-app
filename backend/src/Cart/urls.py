from django.conf.urls import url

from django.urls import path

from .views import (

    cart_view,
    cart_update,
    checkout,
    cart_api_view,
    get_cart,
    modify_cart,
    delete_from_cart

)

urlpatterns = [

    url(r'^$', get_cart, name='CartHome'),
    url(r'^update/$', cart_update, name='CartUpdate'),
    url(r'^checkout/$', checkout, name='CartCheckout'),
    url(r'^api/cart_update/$', cart_api_view, name='cart_api_view'),
    url(r'^modify/$', modify_cart, name='CartModify'),
    url(r'^delete/$',delete_from_cart, name='CartDelete')


]
