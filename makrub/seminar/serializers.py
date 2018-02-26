from rest_framework import serializers
from .models import Room, Answer
from accounts.models import Account
from accounts.serializers import AccountSerializer


class RoomSerializer(serializers.ModelSerializer):
    room_owner = AccountSerializer(read_only=True)
    room_owner_id = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all(),
                                                        write_only=True, source='room_owner',
                                                        allow_null=True, required=False)
    # room_owner = serializers.StringRelatedField() # auto read_only=True, need to declare perform_crate in views.py
    # room_owner = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    guests = serializers.PrimaryKeyRelatedField(many=True, queryset=Account.objects.all())

    class Meta:
        fields = '__all__'
        model = Room

class AnswerSerializer(serializers.ModelSerializer):
    guest_user = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    guest_user_str = serializers.StringRelatedField(source='guest_user')

    class Meta:
        fields = '__all__'
        model = Answer
