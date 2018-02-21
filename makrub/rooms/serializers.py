from rest_framework import serializers
from commons.models import User, Room


class RoomSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source='user_id.username')

    class Meta:
        # fields = (
        #     'id',
        #     'name',
        #     'description',
        #     'user_id',
        #     'survey',
        # )
        fields = '__all__'
        model = Room
