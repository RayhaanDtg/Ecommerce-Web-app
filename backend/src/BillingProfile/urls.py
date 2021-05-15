from django.conf.urls import url

from django.urls import path




from .views import (

    get_billing_profile
   )

urlpatterns = [

    url(r'^$',  get_billing_profile, name='UserBilling')
    

    

]