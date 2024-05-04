from django.contrib import admin
from .models import CustomUser, Topic, Room, RelatedTo, Message

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Topic)
admin.site.register(Room)
admin.site.register(RelatedTo)
admin.site.register(Message)
