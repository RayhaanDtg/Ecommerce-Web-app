from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
# from .models import GuestEmail
from .forms import Login_Form, Register_Form, Guest_Form
from django.contrib.auth import authenticate, login, get_user_model
from .models import User
from rest_framework.decorators import api_view,permission_classes
from ecom.serializers import UserSerializer,MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from django.http import JsonResponse
from rest_framework import status
from rest_framework_jwt.settings import api_settings
from rest_framework.response import Response
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework.authtoken.models import Token


JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

# def guest_login(request):
#     guest_form = Guest_Form(request.POST or None)

#     context = {
#         "form": guest_form

#     }

#     next_ = request.GET.get('next')

#     next_post = request.POST.get('next')

#     redirect_path = next_ or next_post or None

#     if guest_form.is_valid():
#         email = guest_form.cleaned_data.get("email")
#         print(email)
#         new_guest = GuestEmail.objects.create(email=email)
#         request.session['guest_id'] = new_guest.id

#         if is_safe_url(redirect_path, request.get_host()):
#             if redirect_path is not None:
#                 print(redirect_path)
#                 return redirect(redirect_path)

#         else:
#             return redirect('register')

#     return redirect('register')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    queryset = User.objects.all()
    authentication_classes=[JWTAuthentication]
    user_serializer = UserSerializer(queryset, many=True)
    print(request.data)
    json_data = {
        "users": user_serializer.data
    }
    return JsonResponse(json_data)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    data = request.data

    serialized = UserSerializer(data=data)

    if serialized.is_valid():
        print(serialized.data)
        print("we got true")
        email = serialized.data['email']
        firstname = serialized.data['first_name']
        lastname = serialized.data['last_name']
        password = serialized.data['password']
        user = User.objects.create_user(
            email=email, first_name=firstname, last_name=lastname, password=password)
        if user is not None:
            return JsonResponse(serialized.validated_data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        # qs=User.objects.filter(email=email)
        # if qs.exists():
        #     message="Email already exist,"
        # else:
        #     message="Some issue happend. Try again later please"
        # json_data={
        #     "error": serialized.error_messages,
        #     "message":message
        # }
        return JsonResponse(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


# class JWTAuthentication(BaseAuthentication):
#     model=None

#     def get_model(self):
#         return User

#     def authenticate(self,request):
#         auth=request.get_authorization_header(request)
#         if not auth:
#             return None

#         prefix, token= auth.decode('utf-8').split(' ')

#         try:
#             payload=jwt.decode(token, settings.SECRET_KEY)
#         except jwt.DecodeErro

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    # token=MyTokenObtainPairView.get_token()
      





    
# @api_view(['POST'])
# # @csrf_exempt
# def login_user(request):
#     print("got here")
#     data = request.data
#     serialized = UserSerializer(data=data)
#     print(serialized.is_valid())
#     email = serialized.data['email']
#     password = serialized.data['password']
#     user = authenticate(request, email=email, password=password)
#     jwt_token=""
#     # print(user.is_authenticated)
#     if user is not None:
#         try:
#             payload = JWT_PAYLOAD_HANDLER(user)
#             jwt_token = JWT_ENCODE_HANDLER(payload)
#             login(request, user)
#             message = "Logged in successfully"
#         except User.DoesNotExist:
#             message = "User does not exist"
        

#     else:
#         message = "User does not exist"

#     json_data = {
#             "message": message,
#             "token": jwt_token
#         }

#     return JsonResponse(json_data)

# class CustomAuthToken(ObtainAuthToken):

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data,
#                                            context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return JsonResponse({
#             'token': token.key,
#             'user_id': user.id,
#             'email': user.email,
#             'first_name':user.first_name,
#             'last_name':user.last_name
#         })


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
