from django.contrib import admin
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import Group

from .models import UserProfile, Room, RoomAnswer, GuestRoomRelation


User = get_user_model()

# admin.site.unregister(Group)
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Room)
admin.site.register(RoomAnswer)
admin.site.register(GuestRoomRelation)

# To integrate my custom User model with django's admin site, see :
# https://www.fomfus.com/articles/how-to-use-email-as-username-for-django-authentication-removing-the-username
