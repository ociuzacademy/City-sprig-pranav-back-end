from django.contrib import admin
from .models import *
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('name','phone_number','email')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','description','price','quantity','image')
    fields = ('name','description','price','quantity','image')

class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'status')  
    list_filter = ('status',)  
    actions = ['approve_posts','reject_posts']  

    def approve_posts(self, request, queryset):
        """Custom action to approve selected posts"""
        queryset.update(status='approved')
    approve_posts.short_description = "Approve selected posts"  
    
    def reject_posts(self, request, queryset):
        """Custom action to reject selected posts"""
        queryset.update(status='reject')
    reject_posts.short_description = "Reject selected posts"  

# class CartAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'quantity', 'price')  # Fix 'qunatity' to 'quantity'
#     list_filter = ('user', 'status', 'quantity')  # Fix here too
#     fields = ('user','product','qunatity')

class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user','product')
    fields = ('user','product')
    list_filter = ('user','product')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user','product','quantity','price','date','status')
    fields = ('user','product','quantity','price','date','status')
    list_filter = ('user','product','date')

class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('name','description','price','quantity','image')
    fields = ('name','description','price','quantity','image')

admin.site.register(User,UserAdmin)
admin.site.register(Products,ProductAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Recommendation,RecommendationAdmin)
admin.site.register(Wishlist,WishlistAdmin)
admin.site.register(Order,OrderAdmin)