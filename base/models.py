from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
import random

# Create your models here.

class CustomUser(AbstractUser):
    # Generate random user profile image
    def random_image():
        image_urls = [
            'profile_default.jpg',
            'profile_default_2.jpg',
            'profile_default_3.jpg',
            'profile_default_4.jpg',
            'profile_default_5.jpg',
            'profile_default_6.jpg',
            'profile_default_7.jpg',
        ]
        return random.choice(image_urls)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(blank=True, null=True, default=random_image)
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)

    # Specifies the field to be used as the unique identifier for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class RelatedTo(models.Model):
    RELATED_TO = ((0, "Language"), (1, "Framework"), (2, "Library"), (3, "Other"))
    related_to = models.IntegerField(choices=RELATED_TO)

    def __str__(self):
        return dict(self.RELATED_TO)[self.related_to]
    

class Topic(models.Model):
    name = models.CharField(max_length=200)
    topic_related_to = models.ForeignKey(RelatedTo, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

class Room(models.Model):
    host = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="room_host"
    )
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="topic")
    room_related_to = models.ForeignKey(RelatedTo, on_delete=models.CASCADE, related_name="room_related_to")
    participants = models.ManyToManyField(CustomUser, related_name="room_participants", blank=True)
    banned_participants = models.ManyToManyField(CustomUser, related_name="banned_room_participants", blank=True)
    name = models.CharField(max_length=200)
    is_private = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Message(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    image = CloudinaryField('image', blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]