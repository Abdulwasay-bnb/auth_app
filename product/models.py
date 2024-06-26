from datetime import datetime
import uuid
from django.contrib.auth.models import User
from django.http import HttpRequest,HttpResponse
from django.db import models
from members.models import CustomUser
# Create your models here.


class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(auto_now=True)

class Products(BaseModel):
    category_choices = {"Mobile":"Mobile",
                        "Computer":"Computer",
                        "Aaccessories":"Accessories"}
    title = models.CharField(max_length = 200)
    description = models.TextField()
    image = models.ImageField(upload_to ='uploads/')
    category = models.CharField(choices=category_choices,default="Mobile")
    price = models.FloatField(default=0)
    provider = models.ForeignKey('Provider', on_delete=models.CASCADE, null = True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class Provider(models.Model):
    company = models.CharField(max_length = 200, default="")
    location = models.CharField(max_length=200)
    logo = models.ImageField(upload_to ='uploads/')
    details = models.TextField()

class Comments(BaseModel):
    email= models.EmailField(max_length=254)
    comment = models.TextField()
    name = models.CharField(max_length=50, default="")
    product = models.ForeignKey(Products, on_delete=models.CASCADE)


class CommentReply(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    comment_p = models.ForeignKey(Comments, on_delete=models.CASCADE)
    reply = models.TextField()

class Collection(BaseModel):
    product = models.ForeignKey(Products,  on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)

class Customer_Id(BaseModel):
    email = models.EmailField(max_length=254)
    password = models.TextField()
    salt = models.CharField()
    full_name = models.CharField(max_length=50)
    phone_number = models.FloatField(max_length=10)
    phone_code = models.CharField()
    profile_pic = models.ImageField(upload_to ='uploads/', null =True , blank=True)

class Cart(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    quantity  = models.IntegerField(default=0)
    total_price = models.FloatField(default=0.0)

    @property
    def products_summary(self):
        summary = {}
        cart_products = CartProduct.objects.filter(carts=self)
        
        for cart_product in cart_products:
            product = cart_product.product
            if product.uid in summary:
                summary[product.uid] += 1
            else:
                summary[product.uid] = 1
        
        print(summary)
        return summary


class CartProduct(BaseModel):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True, blank=True)
    carts = models.ForeignKey(Cart, on_delete=models.PROTECT, null=True, blank=True)
    # quantity = models.IntegerField(default=0)
    # quantity_wise_price = models.FloatField(default=0.0)