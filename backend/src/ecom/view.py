from django.shortcuts import render, redirect
from django.http import HttpResponse
from .contact_form import Contact_Form
from django.contrib.auth import authenticate, login, get_user_model


# functions to call in the urls.py to map strings to these functions that render a template view

# has a context that contains attributes. This context is then passed with the template to fill in template with
# those attributes

def home_page(request):
    context = {
        "title": "Welcome to the Home Page",
        "content": "content here"
    }
    if request.user.is_authenticated:
        context["premium"] = "Logged in"
    return render(request, "home_page.html", context)


def about_page(request):
    context = {
        "title": "Welcome to the About Page",
        "content": "content here"
    }
    return render(request, "home_page.html", context)


# has a form type from the created class Contact_Form. If the request is a post,
# it is stored in the fields of the form class
# if the form is valid, prints the cleaned_data of the form

def contact_page(request):
    contact_form = Contact_Form(request.POST or None)
    context = {
        "title": "Welcome to the Contact Page",
        "content": "content here",
        "form": contact_form
    }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)

    return render(request, "contact/view.html", context)


