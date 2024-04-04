"""
URL configuration for auth_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include, re_path
from django.conf.urls.static import static
from django.conf import settings

from product.models import Cart
from product.views import custom_404

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Only for demonstration, consider using proper CSRF protection
def last_cart(request):

    if request.method == 'GET':
        try:
            last_cart = Cart.objects.last()
            data = {
                'user_id': last_cart.user.id,
                'quantity': last_cart.quantity,
                'total_price': last_cart.total_price,
                'created_at': last_cart.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': last_cart.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            print(last_cart.products_summary)
            return JsonResponse(data)
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'No carts found'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

print("WASAY")
urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('product.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', include('members.urls')),
    path('api/',include('api.urls')),
    path('last-cart/', last_cart, name='last_cart'),
    re_path(r'^(?!media/|static/).*$', custom_404, name='404-page'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
