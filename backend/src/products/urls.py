

from django.conf.urls import url

from django.urls import path


from .views import (

    # ProductListView,
    product_list_view,

    # ProductSlugDetailView,
    product_slug_view,
    product_id_details
   )

urlpatterns = [

    url(r'^$', product_list_view, name='ProductList'),

    url(r'^(?P<slug>[\w-]+)/$', product_slug_view, name='ProductDetail'),
    url(r'^get_id/(?P<id>\d+)/$',     product_id_details, name='ProductDetailID')

]

