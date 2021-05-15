from django.db import models
from django.conf import settings

from django.db.models.signals import post_save
from account.models import User
# from account.models import GuestEmail

User = settings.AUTH_USER_MODEL


class BillingManager(models.Manager):
    def new_or_get(self, request):
        billing_bool=False
        billing_obj = None
        user = request.user
        # guest_id = request.session.get('guest_id')
        if user.is_authenticated:
            billing_obj, billing_bool = self.model.objects.get_or_create(User=user)

        # elif guest_id is not None:
        #     guest = GuestEmail.objects.get(id=guest_id)

        #     billing_obj, billing_bool = self.model.objects.get_or_create(Email=guest.email)

        else:
            pass
        return billing_obj, billing_bool


class BillingProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)     
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)    
    objects = BillingManager()

    def __str__(self):
        return self.user.email


# def launch_billing(sender, instance, created, *args, **kwargs):
#     if created and instance.email:
#         BillingProfile.objects.get_or_create(user=instance, email=instance.email)


# post_save.connect(launch_billing, sender=User)
