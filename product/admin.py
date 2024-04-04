from django.contrib import admin
from .models import  Products, Provider, Comments , CommentReply, Customer_Id, Cart,CartProduct
# Register your models here.

admin.site.register(Provider)

admin.site.register(Products)

admin.site.register(Comments)

admin.site.register(CommentReply)

admin.site.register(Customer_Id)

admin.site.register(Cart)

admin.site.register(CartProduct)