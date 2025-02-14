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
    


class   ViewCatogories(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        
        return super().list(request, *args, **kwargs)