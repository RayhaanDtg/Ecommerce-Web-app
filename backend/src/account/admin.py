from django.contrib import admin
from django.contrib.auth import get_user_model
from rest_framework.authtoken.admin import TokenAdmin





User=get_user_model()
admin.site.register(User)
TokenAdmin.raw_id_fields = ['user']

