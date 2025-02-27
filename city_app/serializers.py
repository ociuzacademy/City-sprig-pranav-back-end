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

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class ChatHistorySerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = ChatSession
        fields = ['id', 'user_id', 'created_at', 'title']

    def get_title(self, obj):
        latest_message = obj.messages.order_by('-timestamp').first()
        if latest_message:
            words = latest_message.message.split()[:5]  # Get first 5 words
            return ' '.join(words) + '...' if len(words) == 5 else ' '.join(words)
        return "No messages"