from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class Guest_Form(forms.Form):
    email = forms.EmailField()


class Login_Form(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class Register_Form(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField()
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput())

    def clean(self):
        data = self.cleaned_data
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise forms.ValidationError("Password do not match")
        return data

    def clean_username(self):
        data = self.cleaned_data
        username = data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email already exists")
        return email
