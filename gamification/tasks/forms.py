from django import forms
from .models import CustomTask
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class CustomTaskForm(forms.ModelForm):
    class Meta:
        model = CustomTask
        fields = ['title', 'description', 'exp_reward', 'coin_reward']

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1']

class UserLoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)