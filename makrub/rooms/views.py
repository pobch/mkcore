# from django.shortcuts import render

# Create your views here.
from rest_framework import generics

from commons.models import Room
from .serializers import RoomSerializer


class ListRooms(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class DetailRoom(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
