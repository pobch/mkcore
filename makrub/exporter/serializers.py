from rest_framework import serializers
from core.models import RoomAnswer
from api.serializers import RoomAnswerSerializer


missing_value = 'value_missing_when_query'

class RoomAnswerExportSerializer(RoomAnswerSerializer):
    # 'default' will be used if there is no field name when query, not be used if there is a field name
        # but that field's value is null
    room_title = serializers.CharField(source='guest_room_relation.room.title',
        default=missing_value, read_only=True)
    room_description = serializers.CharField(source='guest_room_relation.room.description',
        default=missing_value, read_only=True)
    room_code = serializers.CharField(source='guest_room_relation.room.room_code',
        default=missing_value, read_only=True)
    room_instructor = serializers.CharField(source='guest_room_relation.room.instructor_name',
        default=missing_value, read_only=True)
    room_start_at = serializers.DateTimeField(source='guest_room_relation.room.start_at',
        default=missing_value, read_only=True)
    room_end_at = serializers.DateTimeField(source='guest_room_relation.room.start_at',
        default=missing_value, read_only=True)
    guest_email = serializers.EmailField(source='guest_room_relation.user.email',
        default=missing_value, read_only=True)
    guest_first_name = serializers.CharField(source='guest_room_relation.user.first_name',
        default=missing_value, read_only=True)
    guest_last_name = serializers.CharField(source='guest_room_relation.user.last_name',
        default=missing_value, read_only=True)

    class Meta:
        fields = '__all__'
        model = RoomAnswer


