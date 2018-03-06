from rest_framework import serializers
from core.models import User, Room, Answer


class UserSerializer(serializers.ModelSerializer):
    # own_rooms = serializers.StringRelatedField(many=True, read_only=True)
    # own_rooms = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    # guest_in_rooms = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'
        depth = 1


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


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
