from django.contrib import admin
from .models import CustomUser, Language, Framework, Library, OtherTopic, Topic, Room

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Language)
admin.site.register(Framework)
admin.site.register(Library)
admin.site.register(OtherTopic)
admin.site.register(Topic)
admin.site.register(Room)
