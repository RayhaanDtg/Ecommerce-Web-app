from django.conf.urls import url
from .views import SearchProductView
from django.urls import path


from .views import (

    SearchProductView


   )

urlpatterns = [

    url(r'^$', SearchProductView.as_view(), name='query'),


]

