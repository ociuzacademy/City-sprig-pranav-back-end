from django.shortcuts import get_object_or_404, render
from .models import *
from .serializers import *
from rest_framework import status,viewsets,generics
from rest_framework.response import Response
from rest_framework.views import APIView
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
    serializer_class = WishlistSerializer

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
