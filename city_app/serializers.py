from .models import *
from rest_framework import serializers



class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)  # No unique=True here
    password = serializers.CharField(required=True, write_only=True)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'


class AdminViewUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name','phone_number','email']

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'

class ViewWishlistSerializer(serializers.ModelSerializer):
    product = ProductSerializer() 
        
    class Meta:
        model = Wishlist
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = cart
        fields = '__all__'

class RemoveWishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ['id']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'