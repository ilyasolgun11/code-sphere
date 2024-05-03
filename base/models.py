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


class RelatedTo(models.Model):
    RELATED_TO = ((0, "Language"), (1, "Framework"), (2, "Library"), (3, "Other"))
    related_to = models.IntegerField(choices=RELATED_TO)

    def __str__(self):
        return dict(self.RELATED_TO)[self.related_to]
    

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class Room(models.Model):
    host = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="room_host"
    )
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="topic")
    room_related_to = models.ForeignKey(RelatedTo, on_delete=models.CASCADE, related_name="room_related_to")
    participants = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="room_participants", blank=True, null=True)
    banned_participants = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="banned_room_participants", blank=True, null=True)
    name = models.CharField(max_length=200)
    is_private = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name