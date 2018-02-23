from rest_framework import serializers
from commons.models import Room
from django.contrib.auth.models import User


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

