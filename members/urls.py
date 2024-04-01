from django.urls import path, include
from members.views import sign_up ,login_user, logout_user, change_password

urlpatterns = [
    path('login_user/',login_user,name="login_user"),
    path('logout_user/',logout_user,name="logout"),
    path('sign_up/',sign_up,name="sign_up"), 
    path('change_password/',change_password, name='change_password')
]