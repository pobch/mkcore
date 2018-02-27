from rest_framework import serializers
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    own_rooms = serializers.StringRelatedField(many=True, read_only=True)
    # own_rooms = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    guest_in_rooms = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Account
        fields = '__all__'
        depth = 1


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('email', 'password')

    def create(self, validated_data):
        account = Account.objects.create_user(**validated_data)
        return account


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=200)

    class Meta:
        fields = ('email', 'password')
