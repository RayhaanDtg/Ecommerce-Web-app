from django.conf.urls import url

from django.urls import path




from .views import (

    get_address,
    save_data
   )

urlpatterns = [

    url(r'^$',  get_address, name='UserAddress'),
    url(r'^save/$', save_data, name='SaveAddress'),
    

    

]