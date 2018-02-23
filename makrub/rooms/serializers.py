from rest_framework import serializers
from commons.models import User, Room


class RoomSerializer(serializers.ModelSerializer):
    roomOwner = serializers.StringRelatedField() # auto read_only=True, need to declare perform_crate in views.py
    # roomOwner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        # fields = ()
        fields = '__all__'
        model = Room

