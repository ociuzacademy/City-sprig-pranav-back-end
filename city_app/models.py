from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100,default="")
    phone_number = models.CharField(max_length=12,default="")
    email = models.CharField(max_length=100,default="",unique=True)
    password = models.CharField(max_length=255, default="") 
    
class Products(models.Model):
    name = models.CharField(max_length=100,default="")
    description = models.TextField()
    price = models.DecimalField(decimal_places=2,max_digits=10,null=True,blank=True)
    quantity = models.CharField(max_length=50,default="")
    image = models.FileField(upload_to="product_images",null=True,blank=True)
