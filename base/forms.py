from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Message, Room

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


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants', 'banned_participants']
        widgets = {
            'topic': forms.Select(attrs={'class': 'form-control'}),
            'room_related_to': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'placeholder': 'Enter room name', 'class': 'form-control'}),
            'is_private': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['body', 'image']
        widgets = {
            'body': forms.TextInput(attrs={'placeholder': 'Write your message here...', 'class': 'message-body'}),
            'image': forms.FileInput(attrs={'placeholder': 'Choose an image...', 'class': 'message-file'}),
        }