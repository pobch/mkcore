from rest_framework import serializers
from .models import Room, Answer
from core.models import User


class RoomSerializer(serializers.ModelSerializer):
    room_owner_pk = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        source='room_owner',
        allow_null=True,
        required=False
    )
    # room_owner = serializers.StringRelatedField() # auto read_only=True, need to declare perform_crate in views.py
    # room_owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    guests = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        fields = '__all__'
        model = Room


class AnswerSerializer(serializers.ModelSerializer):
    guest_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    guest_user_str = serializers.StringRelatedField(source='guest_user')

    class Meta:
        fields = '__all__'
        model = Answer
