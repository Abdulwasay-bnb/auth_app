from django.urls import path, include
from django.conf import settings
from product.views import homepage , services , contact_us , about, product_detail,product_list

urlpatterns = [
    path('',homepage,name="home"),
    path('services/',services,name='services'),
    path('about/',about,name="about"),
    path('contact_us/',contact_us,name="contact_us"),
    path('product/<uuid:uid>/', product_detail, name='product_detail'),
    path('product_list/',product_list,name='product_list'),
    ]
