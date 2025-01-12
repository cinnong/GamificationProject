from django import forms
from .models import CustomTask
from .models import DailyTask
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm



class CustomTaskForm(forms.ModelForm):
    class Meta:
        model = CustomTask
        fields = ['title', 'description']

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1']

class UserLoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class DailyTaskForm(forms.ModelForm):
    class Meta:
        model = DailyTask
        fields = ['task', 'day']

from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'banner_image', 'profile_picture']  # Hanya form, bukan model baru

