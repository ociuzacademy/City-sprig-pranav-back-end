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
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    product = models.ForeignKey(Products,on_delete=models.CASCADE,null=True,blank=True)


class cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    product = models.ForeignKey(Products,on_delete=models.CASCADE,null=True,blank=True)
    quantity = models.IntegerField(default=1)

class Post(models.Model):
    CATEGORY_CHOICES = [
        ('question', 'Question'),
        ('discussion', 'Discussion'),
        ('news', 'News'),
        ('announcement', 'Announcement'),
        ('guide', 'Guide'),
        ('meme', 'Meme'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    post = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='discussion')
    status = models.CharField(max_length=30, default='pending')

    def __str__(self):
        return f"{self.user} - {self.category}"

class ChatSession(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)

class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name="messages")
    sender = models.CharField(max_length=10, choices=[('user', 'User'), ('bot', 'Bot')])
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Recommendation(models.Model):
    name = models.CharField(max_length=100,default="")
    description = models.TextField()
    price = models.DecimalField(decimal_places=2,max_digits=10,null=True,blank=True)
    quantity = models.CharField(max_length=50,default="")
    image = models.FileField(upload_to="product_images",null=True,blank=True)
