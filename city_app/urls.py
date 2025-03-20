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
router.register(r'cart', CartView, basename='cart')
router.register(r"wishlist",WishlistView,basename='wishlist')
router.register(r'place_order', PlaceOrderView, basename='place_order')
router.register(r"post",AddPostView,basename="post")

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
    path('view_cart/',ViewCartView.as_view({'get':'list'}),name='view_cart'),
    path('view_wishlist/',ViewWishlistView.as_view({'get':'list'}),name='view_wishlist'),
    path('remove_cart_item/', RemoveCartView.as_view(), name='remove_cart_item'),
    path('remove_wishlist_item/', RemoveWishlistView.as_view(), name='remove_wishlist_item'),
    path('cart/<int:pk>/update_quantity/', UpdateQuantityView.as_view(), name='update_cart_quantity'),
    path('view_posts/',ListPostView.as_view({'get':'list'}),name='view_posts'),
    path('edit_post/',EditPostView.as_view(),name='edit_post'),
    path('delete_post/',DeletePostView.as_view(),name='delete_post'),
    path("start_chat/", start_chat_session, name="start_chat_session"),
    path("chat/<int:session_id>/", chat_with_ai, name="chat_with_ai"),
    path("chat_history/<int:session_id>/", get_chat_history, name="get_chat_history"),
    path("agriculture_advice/", views.get_agriculture_advice, name="get_agriculture_advice"),
    path('check-api-key/', views.check_api_key, name='check_api_key'),
    path('chat_history/',ChatHistoryView.as_view({'get':'list'}),name='chat_history'),
    path('search-posts/', SearchPostView.as_view(), name='search-posts'),
    path("identify-poisonous-plant/", PoisonousPlantCheckView.as_view(), name="identify_poisonous_plant"),
    path("predict-disease/", PlantDiseasePredictionView.as_view(), name="predict_disease"),
    path('view_ordered_items/',ViewOrderedItemsView.as_view({'get':'list'}),name='view_ordered_items'),
    path('identify-plant/', PlantIdentificationView.as_view(), name='identify-plant'),
]