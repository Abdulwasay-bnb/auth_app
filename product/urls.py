from django.urls import path, include
from django.conf import settings
from product.views import homepage , services , contact_us , about, product_detail, product_list, customer_sign_up, customer_login_in, view_cart, add_to_cart, remove_from_cart

urlpatterns = [
    path('',homepage,name="home"),
    path('services/',services,name='services'),
    path('about/',about,name="about"),
    path('contact_us/',contact_us,name="contact_us"),
    path('product/<uuid:uid>/', product_detail, name='product_detail'),
    path('product_list/',product_list,name='product_list'),
    path('customer_sign_up/',customer_sign_up,name='customer_sign_up'),
    path('customer_login_in/',customer_login_in,name="customer_login_in"),
    path('cart/', view_cart, name='view_cart'),
    path('add/<uuid:product_uid>/', add_to_cart, name='add_to_cart'),
    path('remove/<uuid:item_uid>/', remove_from_cart, name='remove_from_cart'),
    ]
