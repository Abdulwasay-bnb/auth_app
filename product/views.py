from datetime import datetime
from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse, HttpResponseNotFound, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Products, Comments, Customer_Id, Cart, CartProduct, CommentReply,Checkout,Address
from django.shortcuts import get_object_or_404
from uuid import UUID
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from django.views.decorators.csrf import csrf_exempt
from dotenv import find_dotenv,load_dotenv
import bcrypt
from django.db.models import Count

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

product_list_path = os.getenv("product_list_path")
# Create your views here.

@login_required
def homepage(request):
    products = Products.objects.all()
    if request.method == 'POST':
        sort_by = request.POST.get('sort_by')
        print("HEEEEEEEEEEE", sort_by)
      
        if sort_by == 'price':
            products= Products.objects.order_by("price")
        
        elif sort_by == 'price_desc':
            products= Products.objects.order_by("price")[::-1]
        
        elif sort_by == 'category':
            products= Products.objects.order_by("category")

        elif sort_by == 'category_desc':
            products= Products.objects.order_by("category")[::-1]
        
        elif sort_by == 'old':
            products = Products.objects.order_by('created_at')[::-1]

        else:
            products = Products.objects.all().order_by('created_at')
    
    cart_product = CartProduct.objects.all()
    product_image = get_object_or_404(Products,uid="7628652e-2741-4a32-a1f3-4971e3abbfa0")
    product_image_2 = get_object_or_404(Products,uid="1e7e53df-2d87-409c-bcc6-a941e5c86396")
    return render(request,"homepage.html", {"products": products, 'cart_product':cart_product,'product_image':product_image,'product_image_2':product_image_2})

def product_detail(request, product_uid):
    product = get_object_or_404(Products, uid=product_uid)
    comments = Comments.objects.filter(product=product)
    comment_ids = comments.values_list('uid', flat=True).distinct('comment_p')
    comments_reply = CommentReply.objects.filter(comment_p__in=comments)
    if request.method == 'POST':
        new_comment = Comments.objects.create(product=product, created_at=datetime.now())
        new_comment.email = request.POST.get('email')
        new_comment.name = request.POST.get('name')
        new_comment.comment = request.POST.get('comment')
        new_comment.product =  product
        new_comment.save()
    return render(request, 'product_detail.html', {'product': product, 'comments':comments,'comments_reply':comments_reply})


def comment_reply(request,comment):
    if request.method == 'POST':
        reply = request.POST.get('reply')
        user = request.user
        new_comment_reply = CommentReply.objects.create(comment_p = comment,reply=reply,user=user)
        new_comment_reply.save()
    

def services(request):
    return render(request,"product.html")


def contact_us(request):
    return render(request,"contact_us.html")


def about(request):
    return render(request,"about.html")

def custom_404(request):
    print("kajkxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxhakdjaklxjklajxkl")
    return render(request, '404.html', status=404)


import requests

def product_list(request):
    # products= Products.objects.all()
    response = requests.get(product_list_path)
    #convert reponse data into json
    products = response.json()
    print(products)
    return render(request,"product_list.html",{'products':products})

@csrf_exempt
def customer_sign_up(request):
    if request.method == "POST":
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        password = request.POST.get('password')
        phone_code = request.POST.get('phone_code')
        phone_number = request.POST.get('phone_number')
        profile_pic = request.FILES.get('image')
        salt = bcrypt.gensalt()
        my_password = password.encode('utf-8')
        hash_password = bcrypt.hashpw(my_password,salt).decode('utf-8')
        salt=salt.decode('utf-8')
        new_Customer_Id = Customer_Id.objects.create(email=email,full_name=full_name,password=hash_password,phone_code=phone_code,phone_number=phone_number,salt=salt,profile_pic=profile_pic)
        new_Customer_Id.save()
    return render(request, 'customer_sign_up.html')

from django.utils.safestring import mark_safe
@csrf_exempt
def customer_login_in(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        my_password = password.encode('utf-8')
        customer = get_object_or_404(Customer_Id, email=email)
        salt = customer.salt
        my_salt =salt.encode('utf-8')
        bcrpyted= bcrypt.hashpw(my_password, my_salt) 
        bcrypted_password = bcrpyted.decode('utf-8')
        if bcrypted_password == customer.password:
            customer = authenticate(email=email, password=bcrypted_password)
            if customer is not None:
                # Log in the user
                login(request, customer)
                messages.success(request, "Successfully registered and logged in")
                render(request, 'home')
                return redirect('home')
            else:
                # Authentication failed
                messages.error(request, "Failed to authenticate user")
                return redirect('home')
        else:
            return render(request, '404.html', status=404)
    return render(request, 'customer_login_in.html')
    
def view_cart(request):
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartProduct.objects.filter(carts=user_cart).distinct('product')
    cart_items_t = CartProduct.objects.filter(carts=user_cart)
    total_price = 0
    total_price = sum(item.product.price  for item in cart_items_t)
    return render(request, 'cart.html', {'cart_items': cart_items, 'user_cart':user_cart,'total_price': total_price})
 
def add_to_cart(request, product_uid):
    product = get_object_or_404(Products, uid=product_uid)
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    cart_product = CartProduct.objects.create(product=product, carts=user_cart)
    # print(cart_product.__dict__)
    # cart_product.quantity += 1
    # cart_product.quantity_wise_price = cart_product.quantity* product.price
    cart_product.save()
    user_cart.save()
    return redirect('view_cart')
 
def remove_from_cart(request, item_uid):
    cart_item = CartProduct.objects.get(uid=item_uid)
    cart_item.delete()
    return redirect('view_cart')


@csrf_exempt
def checkout(request):
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartProduct.objects.filter(carts=user_cart).distinct('product')
    cart_items_t = CartProduct.objects.filter(carts=user_cart)
    total_price = 0
    total_price = sum(item.product.price  for item in cart_items_t)
    address = request.user.address
    if not address or address is None:
        address = Address.objects.create()
        request.user.address = address
        request.user.save()
    
    if request.method == "POST":
        save_address = request.POST.get('save_address')
        phone = request.POST.get('phone')
        checkout = Checkout.objects.get_or_create(user=request.user, address_p = address, cart_p = user_cart,phone = phone)
        print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHIIIIIIIIIIIIIIIIRRRRRRRRRREEEEEEEEEEEE", save_address)
        country = request.POST.get('country')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        address_p = request.POST.get('address')
        address.country=country
        address.city = city
        address.postal_code = postal_code
        address.address_p = address_p
        address.save()
        if save_address == "save_address":
            request.user.address = address
            request.user.save()
    return render(request, 'checkout.html', {'cart_items': cart_items, 'user_cart':user_cart,'total_price': total_price})