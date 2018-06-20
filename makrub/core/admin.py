from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User, UserProfile, Room, RoomAnswer, GuestRoomRelation


admin.site.unregister(Group)
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Room)
admin.site.register(RoomAnswer)
admin.site.register(GuestRoomRelation)
