from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from .models import GuestEmail
from .forms import Login_Form, Register_Form, Guest_Form
from django.contrib.auth import authenticate, login, get_user_model


def guest_login(request):
    guest_form = Guest_Form(request.POST or None)

    context = {
        "form": guest_form

    }

    next_ = request.GET.get('next')

    next_post = request.POST.get('next')

    redirect_path = next_ or next_post or None

    if guest_form.is_valid():
        email = guest_form.cleaned_data.get("email")
        print(email)
        new_guest = GuestEmail.objects.create(email=email)
        request.session['guest_id'] = new_guest.id

        if is_safe_url(redirect_path, request.get_host()):
            if redirect_path is not None:
                print(redirect_path)
                return redirect(redirect_path)

        else:
            return redirect('register')

    return redirect('register')


def login_page(request):
    login_form = Login_Form(request.POST or None)

    context = {
        "form": login_form

    }

    next_ = request.GET.get('next')

    next_post = request.POST.get('next')

    redirect_path = next_ or next_post or None

    if login_form.is_valid():
        username = login_form.cleaned_data.get("username")
        password = login_form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            try:
                del request.session['guest_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                if redirect_path is not None:
                    return redirect(redirect_path)

            else:
                return redirect('home')

        else:
            print("Error")

    return render(request, "accounts/login.html", context)


User = get_user_model()


def register_page(request):
    register_form = Register_Form(request.POST or None)
    context = {
        "form": register_form
    }

    if register_form.is_valid():
        username = register_form.cleaned_data.get("username")
        email = register_form.cleaned_data.get("email")
        password = register_form.cleaned_data.get("password")
        new_user = User.objects.create_user(username, email, password)
        if new_user is not None:
            return redirect('login')

    return render(request, "accounts/register.html", context)
