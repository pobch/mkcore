from rest_framework import serializers
from . import models


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'name',
            'description',
            'user_id',
            'account_id',
            'documents',
        )
        model = models.Room
