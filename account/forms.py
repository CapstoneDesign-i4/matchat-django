from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")
    first_name = forms.CharField(label="이름")
    last_name = forms.CharField(label="전화번호")

    class Meta:
        model=User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
