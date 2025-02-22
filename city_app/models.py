from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100,default="")
    phone_number = models.CharField(max_length=12,default="")
    email = models.CharField(max_length=100,default="",unique=True)
    address = models.CharField(max_length=200,default="",)
    password = models.CharField(max_length=50,default="")

class Products(models.Model):
    name = models.CharField(max_length=100,default="")
    description = models.TextField()
    price = models.DecimalField(decimal_places=2,max_digits=10,null=True,blank=True)
    quantity = models.CharField(max_length=50,default="")
    image = models.FileField(upload_to="product_images",null=True,blank=True)

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    product = models.ForeignKey(Products,on_delete=models.CASCADE,null=True,blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50,default="order")

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True, blank=True, related_name="wishlists")


class cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    product = models.ForeignKey(Products,on_delete=models.CASCADE,null=True,blank=True)
    quantity = models.CharField(max_length=5,default=1)

    