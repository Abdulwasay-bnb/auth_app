from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest,HttpResponse, HttpResponseNotFound, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Products, Comments
from django.shortcuts import get_object_or_404
from uuid import UUID
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def homepage(request):
    products= Products.objects.all()
    return render(request,"homepage.html", {"products": products})

def product_detail(request, uid):
    product = get_object_or_404(Products, uid=uid)
    comments = Comments.objects.all().filter(product=product)
    if request.method == 'POST':
        new_comment = Comments.objects.create(product=product, created_at=datetime.now())
        new_comment.email = request.POST.get('email')
        new_comment.name = request.POST.get('name')
        new_comment.comment = request.POST.get('comment')
        new_comment.product =  product
        new_comment.save()
    return render(request, 'product_detail.html', {'product': product, 'comments':comments})

  
def services(request):
    return render(request,"product.html")


def contact_us(request):
    return render(request,"contact_us.html")


def about(request):
    return render(request,"about.html")


import requests

def product_list(request):
    # products= Products.objects.all()
    response = requests.get('http://localhost:8000/api/')
    #convert reponse data into json
    products = response.json()
    print(products)
    return render(request,"product_list.html",{'products':products})