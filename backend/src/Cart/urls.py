from django.conf.urls import url

from django.urls import path

from .views import (

    cart_view,
    cart_update,
    checkout,
    cart_api_view

)

urlpatterns = [

    url(r'^$', cart_view, name='CartHome'),
    url(r'^update/$', cart_update, name='CartUpdate'),
    url(r'^checkout/$', checkout, name='CartCheckout'),
    url(r'^api/cart_update/$', cart_api_view, name='cart_api_view'),


]
