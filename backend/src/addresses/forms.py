from django.forms import ModelForm
from .models import Address


class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = [

            'address_line_1',
            'city',
            'state',
            'zip_code',
            'country'

        ]
