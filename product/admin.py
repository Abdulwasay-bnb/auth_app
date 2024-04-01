from django.contrib import admin
from .models import Products, Provider, Comments , CommentReply
# Register your models here.

admin.site.register(Provider)

admin.site.register(Products)

admin.site.register(Comments)

admin.site.register(CommentReply)
