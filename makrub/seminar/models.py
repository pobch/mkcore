from django.db import models
from django.contrib.postgres.fields import JSONField
from core.models import User


class Room(models.Model):
    name = models.CharField(max_length=200, verbose_name='this is your room\'s name')
    description = models.TextField()
    # one owner per room
    room_owner = models.ForeignKey(User, related_name='own_rooms', on_delete=models.CASCADE)
    room_login = models.CharField(max_length=200, unique=True, blank=False, null=False)
    room_password = models.CharField(max_length=100, blank=False, null=False)
    guests = models.ManyToManyField(User, related_name='guest_in_rooms')
    survey = JSONField(null=True)

    def __str__(self):
        return self.name


class Answer(models.Model):
    # room = models.ForeignKey()
    guest_user = models.ForeignKey(User, related_name='answers', on_delete=models.CASCADE)
    answer = JSONField(null=True)

    def __str__(self):
        return self.guestUser + ' answers in room: '  # + self.room
