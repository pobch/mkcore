from rest_framework import serializers
from commons.models import Room
from django.contrib.auth.models import User



class AccountSerializer(serializers.ModelSerializer):
    ownRooms = serializers.StringRelatedField(many=True, read_only=True)
    # ownRooms = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    guestInRooms = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = User
        fields = '__all__'
        depth = 1

