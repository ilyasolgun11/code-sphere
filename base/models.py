from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(blank=True, null=True, default="profile_default.jpg")
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)

    # Specifies the field to be used as the unique identifier for authentication
    USERNAME_FIELD = 'email'
    # No additional fields required for creating users
    REQUIRED_FIELDS = ['usernames']