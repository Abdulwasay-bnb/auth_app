from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from members.models import CustomUser
import bcrypt
from .form import RegisterUserForm, SetPasswordForm
from django import forms
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from api.custom_auth import custom_auth

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        print("HEREE")
        # username = request.POST.get('username')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        user = None
        req_user=CustomUser.objects.get(phone=phone_number)
        user = authenticate(request, email=req_user.email,password = password)
        if user is not None:
            login(request, user)
            messages.success(request,("Successfully logged in"))
            print("done")

            return redirect('home')
        else:
            messages.error(request, "Error Logging in: Invalid  phone number, or password")
    else:
        # Handle non-POST requests if needed
        return HttpResponse("Method not allowed", status=404)

@login_required
def logout_user(request):
    logout(request)
    messages.success(request,("Successfully logged out"))
    return redirect('home')

def sign_up(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            salt = bcrypt.gensalt()
            # Create the user object
            user = CustomUser.objects.create_user(email=email, password=password)
            user.phone = phone_number
            user.first_name = first_name
            user.last_name = last_name
            user.salt = salt
            user.save()

            # Authenticate the user
            user = authenticate(email=email, password=password)
            if user is not None:
                # Log in the user
                login(request, user)
                messages.success(request, "Successfully registered and logged in")
                return redirect('home')
            else:
                # Authentication failed
                messages.error(request, "Failed to authenticate user")
    else:
        form = RegisterUserForm()
    return render(request, "authenticate/signup.html", {'form': form})

@login_required
def change_password(request):
    user = request.user
    superAdmin = False
    if request.user.is_superuser:
        superAdmin = True
        email = request.POST.get('email')
        user = None
        if email:
            req_user=CustomUser.objects.get(email=email)
            user = authenticate(request, email=req_user.email)
            if user is not None:
                messages.success(request, "User Found")
            else:
                messages.error(request, "Error : Invalid email")
        if request.method == 'POST':
            form = SetPasswordForm(req_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been changed")
                return redirect('home')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('home')
    else:
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been changed")
                return redirect('home')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('home')
    form = SetPasswordForm(user)
    print("superAdmin", superAdmin)
    return render(request, 'authenticate/change_password.html', {'form': form, "superAdmin": superAdmin})
