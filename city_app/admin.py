from django.contrib import admin
from .models import *
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('name','phone_number','email')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','description','price','quantity','image')
    fields = ('name','description','price','quantity','image')

admin.site.register(User,UserAdmin)
admin.site.register(Products,ProductAdmin)