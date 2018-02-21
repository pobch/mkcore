from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth import get_user_model

User = get_user_model()

class Room(models.Model):
    name = models.CharField(max_length=200,verbose_name='this is your room\'s name')
    description = models.TextField()
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    survey = JSONField(null=True)

    def __str__(self):
        return self.name

