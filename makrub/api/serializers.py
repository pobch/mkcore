from rest_framework import serializers
from core.models import User, UserProfile, Room, RoomAnswer, GuestRoomRelation
from django.core import exceptions
import django.contrib.auth.password_validation as validators


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        extra_kwargs = {'user': {'allow_null': True}}


class RoomSerializer(serializers.ModelSerializer):
    # user_pk = serializers.PrimaryKeyRelatedField(
    #     queryset=User.objects.all(),
    #     write_only=True,
    #     source='user',
    #     allow_null=False,
    #     required=False
    # )
    # user = serializers.StringRelatedField() # auto read_only=True, need to declare perform_create in views.py
    user = serializers.PrimaryKeyRelatedField(read_only=True) # ForeignKey
    guests = serializers.PrimaryKeyRelatedField(many=True, read_only=True) # ManyToMany

    class Meta:
        fields = '__all__'
        model = Room
        extra_kwargs = {'room_password': {'required': False}}


class RoomAnswerSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    # user_str = serializers.StringRelatedField(source='user')
    room = serializers.PrimaryKeyRelatedField(source='guest_room_relation.room', read_only=True)
    guest = serializers.PrimaryKeyRelatedField(source='guest_room_relation.user', read_only=True)

    class Meta:
        fields = '__all__'
        model = RoomAnswer


class UserSerializer(serializers.ModelSerializer):
    # serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    profile = UserProfileSerializer(read_only=True)
    # answers = serializers.HyperlinkedRelatedField(view_name='answer-detail', many=True, read_only=True, allow_null=True)
    # answers = RoomAnswerSerializer(many=True, read_only=True)
    # # StringRelatedField cannot set 'read_only' and 'required' arguments. Use SlugRelatedField instead :
    rooms_owner = serializers.SlugRelatedField(slug_field='title', many=True, read_only=True)
    rooms_owner_links = serializers.HyperlinkedRelatedField(view_name='room-detail', source='rooms_owner', many=True, read_only=True, allow_null=True)
    rooms_guest = serializers.SlugRelatedField(slug_field='title', many=True, read_only=True)
    rooms_guest_links = serializers.HyperlinkedRelatedField(view_name='room-detail', source='rooms_guest', many=True, read_only=True, allow_null=True)

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('last_login', 'is_active', 'is_admin')
        extra_kwargs = {
            'password': {'write_only': True}, # hide password field when GET request
            }

    def validate(self, data):
        super().validate(data)
        if not self.partial: # for 'POST' and 'PUT' method
            user = User(**data)
            password = data.get('password') # get return None by default in case of non-exist key (never throw Error)
            errors = dict() # keys in this dict will be keys in JSON response in case an error occurs
            try:
                validators.validate_password(password=password, user=user)
            except exceptions.ValidationError as e:
                errors['password'] = list(e.messages)
        else: # for 'PATCH' method
            user = User(**data)
            password = data.get('password')
            errors = dict()
            if password is None: # a user dont want to change password
                return data
            else: # a user want to change password
                try:
                    validators.validate_password(password=password, user=user)
                except exceptions.ValidationError as e:
                    errors['password'] = list(e.messages)
        if errors:
                raise serializers.ValidationError(errors) # add to JSON
        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

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


class GuestRoomRelationSerializer(serializers.ModelSerializer):
    room_title = serializers.CharField(source='room.title', read_only=True)
    room_room_code = serializers.CharField(source='room.room_code', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_first_name = serializers.CharField(source='user.first_name', read_only=True)
    user_last_name = serializers.CharField(source='user.last_name', read_only=True)
    answer_submitted_at = serializers.DateTimeField(source='answer_detail.submitted_at', read_only=True)

    class Meta:
        model = GuestRoomRelation
        fields = '__all__'
