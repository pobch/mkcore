from rest_framework import serializers
from seminar.models import Room
from .models import Account



class AccountSerializer(serializers.ModelSerializer):
    own_rooms = serializers.StringRelatedField(many=True, read_only=True)
    # own_rooms = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    guest_in_rooms = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Account
        fields = '__all__'
        depth = 1

