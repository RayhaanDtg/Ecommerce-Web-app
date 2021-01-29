

from django.conf.urls import url

from django.urls import path


from .views import (

    ProductListView,

    ProductSlugDetailView,
   )

urlpatterns = [

    url(r'^$', ProductListView.as_view(), name='ProductList'),

    url(r'^(?P<slug>[\w-]+)/$', ProductSlugDetailView.as_view(), name='ProductDetail')
]

