from rest_framework.response import Response
from rest_framework.decorators import api_view
from members.models import CustomUser
from product.models import Products, Provider
from .serializers import ProductSerializer, ProviderSerializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

@api_view(['GET'])
def getData(request):
    products= Products.objects.all()
    serializer = ProductSerializer(products,many=True)
    return Response(serializer.data)

# @api_view(['POST'])
@csrf_exempt
def add_data(request):
    if request.method =='POST':
        title=request.POST.get('title')
        description=request.POST.get('description')
        price=int(request.POST.get('price'))
        category=request.POST.get('category')
        email=request.POST.get('email')
        user = CustomUser.objects.get(email=email)
        image = request.FILES.get('image')
        product = Products.objects.create(title=title, description=description, price=price, category=category, created_by=user, image=image)
        serializer = ProductSerializer(product)
        return JsonResponse(serializer.data, status=201)
    else:
        return JsonResponse({'error': 'Bad Request'}, status=400)


@csrf_exempt
def delete_product(request,uid):
    product= get_object_or_404(Products,uid=uid)
    if request.method == 'POST':
        product.delete()
        return JsonResponse({'message': 'Product deleted successfully'}, status=200)
    else:
        JsonResponse({'error': 'Bad Request'}, status=400)
        

@csrf_exempt
def editpost(request, uid):
    product = get_object_or_404(Products, uid=uid)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = float(request.POST.get('price'))
        category = request.POST.get('category')
        image = request.FILES.get('image')
        product.title = title
        product.description = description
        product.price = price
        product.category = category
        product.image = image
        product.save()
        return JsonResponse({'message': 'Product updated successfully'})
    else:
        return JsonResponse({'error': 'Bad Request'}, status=400)