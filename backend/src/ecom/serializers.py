from rest_framework import serializers
from Cart.models import Cart
from products.models import Product
from Order.models import Order
from account.models import User
from addresses.models import Address
from BillingProfile.models import BillingProfile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from stock.models import Stock
from CartItem.models import CartItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields= '__all__'

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model=Stock
        fields= '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cart
        fields= '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields='__all__'
        
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields= '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields= '__all__'

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model=Address
        fields='__all__'


class BillingSerializer(serializers.ModelSerializer):
    class Meta:
        model=BillingProfile
        fields='__all__'

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
      
        token['email'] = user.email
        token['first_name']=user.first_name
        token['last_name']=user.last_name
        return token

