"""ecom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from .view import about_page
from .view import contact_page
from .view import home_page
from account.views import login_page, register_page
from addresses.views import checkout_address, reuse_address
# from BillingProfile.views import 


# from products.views import (
#     product_list_view,
#     ProductListView,
#     ProductDetailView,
#     product_detail_view,
#     ProductFeatureListView,
#     ProductSlugDetailView,
#     ProductFeatureDetailView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name='home'),
    path('about/', about_page, name='about'),
    path('contact/', contact_page, name='contact'),
    path('login/', login_page, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register_page, name='register'),
    # path('register/guest/', guest_login, name='guest_register'),
    path('address/', checkout_address, name='checkout_address'),
    path('reuse/address/', reuse_address, name='reuse_address'),
    url(r'^products/', include(("products.urls", 'products'), namespace='products')),
    url(r'^search/', include(("search.urls", 'search'), namespace='search')),
    url(r'^Cart/', include(("Cart.urls", 'Cart'), namespace='Cart')),
    url(r'^Users/', include(("account.urls", 'Users'), namespace='Users')),
    url(r'^BillingProfile/', include(("BillingProfile.urls", 'BillingProfile'), namespace='BillingProfile')),
    url(r'^Address/', include(("addresses.urls", 'Address'), namespace='Address')),



    # path('products-fbv/', product_list_view),
    # # url(r'^products/(?P<pk>\d+)/$', ProductDetailView.as_view()),  # use url for regex expressions
    # url(r'^products-fbv/(?P<pk>\d+)/$', product_detail_view),
    # url(r'^in-stock/(?P<pk>\d+)/$', ProductFeatureDetailView.as_view()),
    # path('in-stock/', ProductFeatureListView.as_view()),
    # url(r'^products/(?P<slug>[\w-]+)/$', ProductSlugDetailView.as_view())
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
