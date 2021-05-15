from django.conf.urls import url

from django.urls import path
from rest_framework_simplejwt.views import (
   
    TokenRefreshView,
    TokenVerifyView
)
# from ecom.serializers import MyTokenObtainPairView


from .views import (

    get_user,
    register_user,
     MyTokenObtainPairView,
    #  login_user
    
    # CustomAuthToken
   )

urlpatterns = [

    url(r'^$', get_user, name='UserList'),
    url(r'^register/$', register_user, name='RegisterUser'),
    url(r'^login/$',MyTokenObtainPairView.as_view(),name='LoginUser'),
    # url(r'^login/', CustomAuthToken.as_view(), name='CustomAuthToken'),
    # url(r'^api/token/$',login_user, name='token_obtain_pair'),
    url(r'^refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
    url(r'^api/token/verify/$', TokenVerifyView.as_view(), name='token_verify'),

    

]

