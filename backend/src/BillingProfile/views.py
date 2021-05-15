from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from .models import BillingProfile,BillingManager
from ecom.serializers import BillingSerializer

from account.models import User
from rest_framework.decorators import api_view,permission_classes

from django.http import JsonResponse
from rest_framework import status
from rest_framework_jwt.settings import api_settings
from rest_framework.response import Response
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication


JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_billing_profile(request):
    data=request.data
    email=data['email']
    user=User.objects.filter(email=email)
    if user is not None:
        billing_obj,billing_bool= BillingProfile.objects.get_or_create(user=user.first())
    else:
        billing_obj=None

    billing_serializer=BillingSerializer(billing_obj)
    
    json_data={
        "billing_profile": billing_serializer.data
    }

    return JsonResponse(json_data)

