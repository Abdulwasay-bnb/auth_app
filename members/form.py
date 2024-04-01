from django.contrib.auth.forms import UserCreationForm,SetPasswordForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import get_user_model


class RegisterUserForm(forms.Form):
    email = forms.EmailField()
    phone_number = forms.CharField(max_length = 13)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    
    class Meta:
        model = User
        fields = ('phone_number','first_name','last_name','email','password')


class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']
