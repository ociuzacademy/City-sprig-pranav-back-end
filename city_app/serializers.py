from .models import *
from rest_framework import serializers



class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','password']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'


class AdminViewUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name','phone_number','email']

