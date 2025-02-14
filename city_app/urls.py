from django.contrib import admin
from .import views
from django.urls import path,include,re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from  rest_framework.routers import DefaultRouter
from .views import *


schema_view = get_schema_view(
    openapi.Info(
        title="City Spring API",
        default_version="v1",
        description="API documentation for the City Spring app.",
        terms_of_service="https://www.google.com/policies/terms/",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = DefaultRouter()
router.register(r"user_register",UserRegistrationView,basename="user_register")
router.register(r"add_product",AddProducts,basename='add_product')

urlpatterns = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),

    path('',include(router.urls)),
    path('login/',LoginView.as_view(),name='login'),
    path('user_view_profile/',UserProfileView.as_view({'get':'list'}),name='user_view_profile'),
    path('update_profile/',UpdateProfileView.as_view(),name='update_profile'),
    path('view_users/',AdminViewUsersView.as_view({'get':'list'}),name='view_users'),
    path('view_product/',ViewProductByIdView.as_view({'get':'list'}),name='view_product'),
    path('list_products/',ViewProductsListView.as_view({'get':'list'}),name='list_products'),
    path('search_product/',SearchProductView.as_view({'get':'list'}),name='search_product'),
]