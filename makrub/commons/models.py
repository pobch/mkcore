from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User


class Room(models.Model):
    name = models.CharField(max_length=200,verbose_name='this is your room\'s name')
    description = models.TextField()
    # one owner per room
    roomOwner = models.ForeignKey(User, related_name='ownRooms', on_delete=models.CASCADE)
    roomLogin = models.CharField(max_length=200, unique=True, blank=False, null=False)
    roomPassword = models.CharField(max_length=100, blank=False, null=False)
    guests = models.ManyToManyField(User, related_name='guestInRooms')
    survey = JSONField(null=True)

    def __str__(self):
        return self.name


class Answer(models.Model):
    # room = models.ForeignKey()
    guestUser = models.ForeignKey(User, related_name='answers', on_delete=models.CASCADE)
    answer = JSONField(null=True)

    def __str__(self):
        return self.guestUser + ' answers in room: ' # + self.room
