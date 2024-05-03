from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

# Custom form for user creation
class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter your username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
            'password1': forms.PasswordInput(attrs={'placeholder': '&bull;&bull;&bull;&bull;&bull;&bull;&bull;&bull;'}),
            'password2': forms.PasswordInput(attrs={'placeholder': '&bull;&bull;&bull;&bull;&bull;&bull;&bull;&bull;'}),
        }