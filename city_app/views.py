from django.conf import settings
from django.shortcuts import get_object_or_404, render
from .models import *
from .serializers import *
from rest_framework import status,viewsets,generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.postgres.search import TrigramSimilarity
# Create your views here.


class UserRegistrationView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            response_data = {
                "status": "success",
                "message": "User created successfully"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                "status": "failed",
                "message": "Invalid Details",
                "errors": serializer.errors
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            try:
                user = User.objects.get(email=email)
                if password == user.password:
                    response_data = {
                        "status": "success",
                        "message": "User logged in successfully",
                        "user_id": str(user.id)
                    }
                    request.session['id'] = user.id
                    return Response(response_data, status=status.HTTP_200_OK)
                else:
                    return Response({"status": "failed", "message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                return Response({"status": "failed", "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"status": "failed", "message": "Invalid input"}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def list(self, request, *args, **kwargs):
        user_id = request.query_params.get('id')
        print("Query parameters received:", request.query_params)

        if not user_id:
            response_data = {
                "status": "failed",
                "message": "User ID is required."
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
            print("User found:", user)
        except User.DoesNotExist:
            print("User with ID", user_id, "does not exist in the database.")
            response_data = {
                "status": "failed",
                "message": "User does not exist."
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        serializer = UserRegisterSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class UpdateProfileView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    http_method_names = ['patch']

    def patch(self, request, *args, **kwargs):
        user_id = request.data.get('id')

        if not user_id:
            response_data = {
                "status": "failed",
                "message": "User ID is required."
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, id=user_id)

        # Pass request data to the serializer
        serializer = UserRegisterSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save() 
            return Response(
                {"status": "success", "message": "Profile updated successfully"},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"status": "failed", "message": "Invalid details", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )



class AddProducts(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        
        data = request.data.copy()

        print(data)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            response_data = {
                "status": "success",
                "message": "Product added successfully"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                "status": "failed",
                "message": "Invalid Details",
                "errors": serializer.errors
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class AdminViewUsersView(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminViewUsersSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

class ViewProductByIdView(viewsets.ReadOnlyModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        product_id = request.query_params.get("id")

        if product_id:
            try:
                product = self.queryset.get(id=product_id)
                serializer = self.get_serializer(product)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Products.DoesNotExist:
                return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)


class ViewProductsListView(viewsets.ReadOnlyModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class SearchProductView(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        name = request.query_params.get('name', None)
        print("Query parameter received:", name)
        
        if name:
            products = Products.objects.filter(course_name__icontains=name)
            print("Filtered courses:", products)
        else:
            products = Products.objects.all()
            print("All courses:", products)

        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class BuyProduct(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user')
        product_id = request.data.get('product')
        quantity = int(request.data.get('quantity', 1))  # Default quantity is 1
        
        if not user_id:
            return Response(
                {"status": "failed", "message": "User ID not provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not product_id:
            return Response(
                {"status": "failed", "message": "Product ID not provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate User
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"status": "failed", "message": "User not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Validate Product
        try:
            product = Products.objects.get(id=product_id)
        except Products.DoesNotExist:
            return Response(
                {"status": "failed", "message": "Product not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Check product availability
        if quantity <= 0:
            return Response(
                {"status": "failed", "message": "Invalid quantity."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if int(product.quantity) < quantity:
            return Response(
                {"status": "failed", "message": "Insufficient product quantity."},
                status=status.HTTP_400_BAD_REQUEST,
            )


        # Calculate total price
        total_price = product.price * quantity

        # Reduce product quantity
        product.quantity = str(int(product.quantity) - quantity)
        product.save()
        print(request.data)
        # Prepare purchase data
        purchase_data = {
            "user": user.id,
            "product": product.id,
            "quantity": quantity,
            "price": total_price,
        }
        # print(purchase_data)

        serializer = self.get_serializer(data=purchase_data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "message": "Product purchased successfully", "data": serializer.data},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"status": "failed", "message": "Purchase failed", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )



# class   ViewCatogories(viewsets.ModelViewSet):
#     def list(self, request, *args, **kwargs):
        
#         return super().list(request, *args, **kwargs)



class WishlistView(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                self.perform_create(serializer)
                return Response(
                    {"status": "success", "message": "Product added to wishlist successfully"},
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response(
                    {"status": "failed", "message": "An error occurred", "error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(
            {"status": "failed", "message": "Invalid Details", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

class ViewWishlistView(viewsets.ReadOnlyModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = ViewWishlistSerializer

    def list(self, request, *args, **kwargs):
        user_id = request.query_params.get('id')
        print("Query parameters received:", request.query_params)

        if user_id:
            # Filter products by the provided service_centre_id
            products = self.queryset.filter(user_id=user_id)
        else:
            # Return an error response if 'service_centre' is not provided
            response_data = {
                "status": "failed",
                "message": "User ID is required."
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        # Serialize the filtered queryset
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

class RemoveWishlistView(generics.DestroyAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer

    def destroy(self, request, *args, **kwargs):
        wishlist_item_id = request.data.get('id')
        try:
            wishlist_item = Wishlist.objects.get(id=wishlist_item_id)
            wishlist_item.delete()
            return Response(
                {"status": "success", "message": "Product removed from wishlist successfully"},
                status=status.HTTP_200_OK
            )
        except Wishlist.DoesNotExist:
            return Response(
                {"status": "failed", "message": "Wishlist item not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"status": "failed", "message": "An error occurred", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CartView(viewsets.ModelViewSet):
    queryset = cart.objects.all()
    serializer_class = CartSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user')
        product_id = request.data.get('product')
        quantity = request.data.get('quantity', 1)

        if not user_id or not product_id:
            return Response(
                {"status": "failed", "message": "User and Product are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            product = Products.objects.get(id=product_id)

            # Ensure quantity is valid
            if int(quantity) <= 0:
                return Response(
                    {"status": "failed", "message": "Quantity must be greater than 0"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Check if product is already in the cart
            cart_item, created = cart.objects.get_or_create(user_id=user_id, product_id=product_id)
            
            if not created:
                # Update the quantity if the product is already in the cart
                cart_item.quantity = str(int(cart_item.quantity) + int(quantity))
                cart_item.save()

            return Response(
                {"status": "success", "message": "Product added to cart successfully"},
                status=status.HTTP_201_CREATED
            )

        except Products.DoesNotExist:
            return Response(
                {"status": "failed", "message": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"status": "failed", "message": "An error occurred", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

class ViewCartView(viewsets.ReadOnlyModelViewSet):
    queryset = cart.objects.all()
    serializer_class = CartSerializer

    def list(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id')
        print("Query parameters received:", request.query_params)

        if not user_id:
            return Response({
                "status": "failed",
                "message": "User ID is required."
            }, status=status.HTTP_400_BAD_REQUEST)

        products = self.queryset.filter(user_id=user_id)
        if not products.exists():
            return Response({
                "status": "failed",
                "message": "No cart items found for this user."
            }, status=status.HTTP_404_NOT_FOUND)

        cart_items = []
        total_price = 0

        for item in products:
            cart_items.append({
                "product": item.product.id,
                "quantity": item.quantity,
                "name":item.product.name,
                "image":item.product.image.url if item.product.image else None,
                "price":item.product.price if item.product.price else 0
            })
            total_price += float(item.product.price) * int(item.quantity) if item.product.price else 0

        response_data = {
            "user": user_id,
            "cart_items": cart_items,
            "totalPrice": total_price
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    

class RemoveCartView(generics.DestroyAPIView):
    queryset = cart.objects.all()
    serializer_class = CartSerializer

    def destroy(self, request, *args, **kwargs):
        cart_item_id = request.data.get('id')
        try:
            cart_item = cart.objects.get(id=cart_item_id)
            cart_item.delete()
            return Response(
                {"status": "success", "message": "Product removed from cart successfully"},
                status=status.HTTP_200_OK
            )
        except cart.DoesNotExist:
            return Response(
                {"status": "failed", "message": "Cart item not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"status": "failed", "message": "An error occurred", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UpdateQuantityView(generics.UpdateAPIView):
    queryset = cart.objects.all()
    serializer_class = CartSerializer
    http_method_names = ['patch',]

    def patch(self, request, *args, **kwargs):
        """
        API to increase or decrease the quantity of a product in the cart.
        """
        cart_id = kwargs.get('pk')  # Get the cart item ID from URL parameters
        action_type = request.data.get('action')  # 'increase' or 'decrease'

        try:
            cart_item = cart.objects.get(pk=cart_id)

            if action_type == 'increase':
                cart_item.quantity = int(cart_item.quantity) + 1
            elif action_type == 'decrease':
                if int(cart_item.quantity) > 1:
                    cart_item.quantity = int(cart_item.quantity) - 1
                else:
                    return Response(
                        {"status": "failed", "message": "Quantity cannot be less than 1"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {"status": "failed", "message": "Invalid action. Use 'increase' or 'decrease'"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            cart_item.save()
            return Response(
                {"status": "success", "message": "Quantity updated successfully", "quantity": cart_item.quantity},
                status=status.HTTP_200_OK
            )

        except cart.DoesNotExist:
            return Response(
                {"status": "failed", "message": "Cart item not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"status": "failed", "message": "An error occurred", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class PlaceOrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    http_method_names = ["post"]  # Restrict to only POST requests

    def create(self, request, *args, **kwargs):
        user_id = request.data.get("user")

        if not user_id:
            return Response(
                {"status": "failed", "message": "User ID not provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate User
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"status": "failed", "message": "User not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Fetch all cart items for the user
        cart_items = cart.objects.filter(user=user)
        if not cart_items.exists():
            return Response(
                {"status": "failed", "message": "Cart is empty."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        order_list = []
        for item in cart_items:
            product = item.product
            quantity = int(item.quantity)

            # Check if product has enough stock
            if product.quantity < quantity:
                return Response(
                    {
                        "status": "failed",
                        "message": f"Insufficient stock for {product.name}. Only {product.quantity} available.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Calculate total price
            total_price = product.price * quantity

            # Reduce product quantity
            product.quantity -= quantity
            product.save()

            # Create order data
            order_data = {
                "user": user.id,
                "product": product.id,
                "quantity": quantity,
                "price": total_price,
                "status": "ordered",
            }

            order_list.append(order_data)

        # Bulk create orders
        serializer = self.get_serializer(data=order_list, many=True)
        if serializer.is_valid():
            serializer.save()
            # Clear the cart after order placement
            cart_items.delete()
            return Response(
                {"status": "success", "message": "Order placed successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"status": "failed", "message": "Order placement failed", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
    

class AddPostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            response_data = {
                "status": "success",
                "message": "Post added successfully"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                "status": "failed",
                "message": "Invalid Details",
                "errors": serializer.errors
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class SearchPostView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', None)
        if query:
            return Post.objects.annotate(similarity=TrigramSimilarity('post', query)) \
                .filter(similarity__gt=0.2) \
                .order_by('-similarity')
        return Post.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ListPostView(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        posts = Post.objects.filter(status='approved')
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class EditPostView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def patch(self, request, *args, **kwargs):

        post_id = request.data.get('id')
        try:
            post = Post.objects.get(id=post_id)  # Retrieve the Employee object
        except Post.DoesNotExist:
            return Response(
                {"status": "failed", "message": "Post not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": "success",
                    "message": "Post updated successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "status": "failed",
                    "message": "Invalid Details",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
class DeletePostView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def destroy(self, request, *args, **kwargs):
        post_id = request.data.get('id')
        try:
            post = Post.objects.get(id=post_id)
            post.delete()
            return Response(
                {"status": "success", "message": "Post deleted successfully"},
                status=status.HTTP_200_OK
            )
        except Post.DoesNotExist:
            return Response(
                {"status": "failed", "message": "Post not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"status": "failed", "message": "An error occurred", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
from django.http import JsonResponse
from django.conf import settings

def check_api_key(request):
    # Print the API key to confirm it's loaded correctly
    api_key = settings.GOOGLE_AI_API_KEY
    print(f"API Key: {api_key}")  # In production, consider using logging instead of print()
    
    if api_key:
        return JsonResponse({"status": "API Key is set", "api_key": api_key})
    else:
        return JsonResponse({"status": "API Key is not set"})


# import google.generativeai as genai

# genai.configure(api_key=settings.GOOGLE_AI_API_KEY)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import google.generativeai as genai
from .models import ChatSession, ChatMessage
import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GOOGLE_AI_API_KEY)
@api_view(["POST"])
def start_chat_session(request):
    """Starts a new chat session for the user"""
    user_id = request.data.get("user_id")  # Ensure you get user_id from frontend
    session = ChatSession.objects.create(user_id=user_id)
    return Response({"session_id": session.id}, status=status.HTTP_201_CREATED)

@api_view(["POST"])
def chat_with_ai(request, session_id):
    """Handles chatbot interaction with chat history"""
    try:
        session = ChatSession.objects.get(id=session_id)
        user_message = request.data.get("message")

        # Store user message in DB
        ChatMessage.objects.create(session=session, sender="user", message=user_message)

        # Retrieve previous messages for context
        previous_messages = ChatMessage.objects.filter(session=session).order_by("timestamp")

        # Format chat history for AI
        conversation_history = "\n".join(
            [f"{msg.sender}: {msg.message}" for msg in previous_messages]
        )

        # Generate AI response
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        response = model.generate_content(conversation_history + f"\nUser: {user_message}\nBot:")

        bot_reply = response.text.strip()

        # Store bot response in DB
        ChatMessage.objects.create(session=session, sender="bot", message=bot_reply)

        return Response({"reply": bot_reply}, status=status.HTTP_200_OK)

    except ChatSession.DoesNotExist:
        return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(["GET"])
def get_chat_history(request, session_id):
    """Fetches chat history for a given session"""
    try:
        session = ChatSession.objects.get(id=session_id)
        messages = ChatMessage.objects.filter(session=session).order_by("timestamp")
        chat_history = [{"sender": msg.sender, "message": msg.message, "timestamp": msg.timestamp} for msg in messages]
        return Response({"chat_history": chat_history}, status=status.HTTP_200_OK)
    except ChatSession.DoesNotExist:
        return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)
    
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import google.generativeai as genai
import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GOOGLE_AI_API_KEY)
@api_view(["POST"])
def get_agriculture_advice(request):
    """Provides remedies and crop recommendations for a given plant disease"""
    try:
        disease_name = request.data.get("disease")

        if not disease_name:
            return Response({"error": "Disease name is required"}, status=status.HTTP_400_BAD_REQUEST)

        # AI prompt for an agriculture expert response
        prompt = f"""
        Act as an agriculture expert. A farmer has identified a plant disease: {disease_name}.
        - Provide effective remedies to cure or prevent the disease.
        - Suggest alternative crops that are more resistant to this disease.
        - If applicable, recommend organic or chemical treatments and best farming practices.
        """

        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        response = model.generate_content(prompt)
        ai_response = response.text.strip()

        return Response({"disease": disease_name, "advice": ai_response}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class ChatHistoryView(viewsets.ReadOnlyModelViewSet):
    queryset = ChatSession.objects.prefetch_related('messages').all()
    serializer_class = ChatHistorySerializer

    def list(self, request, *args, **kwargs):
        user_id = request.query_params.get('id')
        print("Query parameters received:", request.query_params)

        if user_id:
            history = self.queryset.filter(user_id=user_id)
        else:
            response_data = {
                "status": "failed",
                "message": "User ID is required."
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
