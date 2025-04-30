from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class Register(UserCreationForm):
    password2 =forms.CharField(label='Confirm Password',widget=forms.PasswordInput)
    class Meta:
        model=User
        # fields = '__all__'
        fields = ['username','first_name','last_name']