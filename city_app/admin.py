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

class CartAdmin(admin.ModelAdmin):
    list_display = ('user','product','qunatity')
    fields = ('user','product','qunatity')
    list_filter = ('user','product','qunatity')

class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user','product')
    fields = ('user','product')
    list_filter = ('user','product')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('')

admin.site.register(User,UserAdmin)
admin.site.register(Products,ProductAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(cart,CartAdmin)
admin.site.register(Wishlist,WishlistAdmin)