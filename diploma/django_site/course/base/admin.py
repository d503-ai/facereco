from django.contrib import admin

# ADMIN - ROOT
# PASS  - ROOT

from .models import Room, Topic, Message

admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)

