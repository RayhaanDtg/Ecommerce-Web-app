from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


# class that creates a Django form and inserts fields to the form.
# the posted data then gets stores in those fields with specific id's
# each form object can have a specific type, for example CharField can be a widget of type Textarea
class Contact_Form(forms.Form):
    fullname = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "id": "full_name", "placeholder": "Your Name"}))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "id": "email", "placeholder": "Your email"})
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "id": "content", "placeholder": "About you"}))

    # this function checks if a field is valid when the is_valid() function is called on cleaned_data here if there is a
    # mistake, a validation error will be raised. it takes parameters self so that later the self.cleaned_data can be
    # invoked. then a python object is being passed, and not strings

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not "gmail.com" in email:
            raise forms.ValidationError("Email should be gmail")

        return email


