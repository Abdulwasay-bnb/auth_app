from django.urls import path
from .views import getData, add_data,editpost,delete_product

urlpatterns = [
    path('',getData,name='getData'),
    path('add/',add_data,name='add_data'),
    path('editpost/<uuid:uid>/',editpost,name='editpost'),
    path('delete_product/<uuid:uid>/',delete_product,name='delete_product')
]