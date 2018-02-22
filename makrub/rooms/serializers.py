from rest_framework import serializers
from commons.models import User, Room


class RoomSerializer(serializers.ModelSerializer):
    user_id = serializers.StringRelatedField() # auto read_only=True, need to declare perform_crate in views.py
    # user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        # fields = (
        #     'id',
        #     'name',
        #     'description',
        #     'user_id',
        #     'survey',
        # )
        fields = '__all__'
        model = Room

