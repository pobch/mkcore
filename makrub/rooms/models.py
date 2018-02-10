from django.db import models

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    user_id = models.IntegerField()
    account_id = models.IntegerField()
    documents = models.TextField()

    def __str__(self):
        return self.name
