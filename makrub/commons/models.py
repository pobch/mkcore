from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth import get_user_model

User = get_user_model()

class Room(models.Model):
    name = models.CharField(max_length=200,verbose_name='this is your room\'s name')
    description = models.TextField()
    # one owner per room
    roomOwner = models.ForeignKey(User, related_name='ownRooms', on_delete=models.CASCADE)
    roomLogin = models.CharField(max_length=200, unique=True, blank=False, null=False)
    roomPassword = models.CharField(max_length=100, blank=False, null=False)
    guests = models.ManyToManyField(User, related_name='guestRooms', blank=True)
    survey = JSONField(null=True)

    def __str__(self):
        return self.name

