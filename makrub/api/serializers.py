from rest_framework import serializers
from core.models import User, UserProfile, Room, RoomAnswer


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        extra_kwargs = {'user': {'allow_null': True}}


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
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = '__all__'
        # extra_kwargs = {'password': {'write_only': True}} # hide password field when GET request

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate(self, data):
        try:
            new_password = data['password']
        except KeyError:
            new_password = None
            print('The user did not want to change their password (new password is not provided)')
        if new_password:
            print('The password is provided, check with confirm password here')
        return data

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.is_admin = validated_data.get('is_admin', instance.is_admin)
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


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
