# from django.shortcuts import render

# Create your views here.
from rest_framework import generics

from . import models
from . import serializers


class ListRooms(generics.ListCreateAPIView):
    queryset = models.Room.objects.all()
    serializer_class = serializers.RoomSerializer

class DetailRoom(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Room.objects.all()
    serializer_class = serializers.RoomSerializer
