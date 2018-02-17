from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=200,verbose_name='this is your room\'s name')
    description = models.TextField()
    user_id = models.IntegerField()
    account_id = models.IntegerField()
    documents = JSONField(null=True)

    def __str__(self):
        return self.name
