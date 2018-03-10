from rest_framework import serializers
from core.models import User, UserProfile, Room, RoomAnswer


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    # own_rooms = serializers.StringRelatedField(many=True, read_only=True)
    # own_rooms = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    # guest_in_rooms = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = User
        fields = '__all__'
        depth = 1
        extra_kwargs = {'password': {'write_only': True}} # hide password field when GET request


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    # user_pk = serializers.PrimaryKeyRelatedField(
    #     queryset=User.objects.all(),
    #     write_only=True,
    #     source='user',
    #     allow_null=False,
    #     required=False
    # )
    # user = serializers.StringRelatedField() # auto read_only=True, need to declare perform_create in views.py
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    guests = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        fields = '__all__'
        model = Room


class AnswerSerializer(serializers.ModelSerializer):
    # guest_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    # guest_user_str = serializers.StringRelatedField(source='guest_user')

    class Meta:
        fields = '__all__'
        model = RoomAnswer
