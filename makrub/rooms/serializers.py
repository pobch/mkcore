from rest_framework import serializers
from commons.models import User, Room, Answer
from accounts.serializers import AccountSerializer


class RoomSerializer(serializers.ModelSerializer):
    roomOwner = AccountSerializer(read_only=True)
    roomOwner_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),
                                                        write_only=True, source='roomOwner',
                                                        allow_null=True, required=False)
    # roomOwner = serializers.StringRelatedField() # auto read_only=True, need to declare perform_crate in views.py
    # roomOwner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    guests = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        # fields = ()
        fields = '__all__'
        model = Room

class AnswerSerializer(serializers.ModelSerializer):
    guestUser = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    guestUser_str = serializers.StringRelatedField(source='guestUser')

    class Meta:
        fields = '__all__'
        model = Answer
