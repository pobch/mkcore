# import uuid
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view

from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode

from core.models import User, Room, RoomAnswer, UserProfile
from api.serializers import UserSerializer, UserProfileSerializer, RoomSerializer, RoomAnswerSerializer
from api.tokens import account_activation_token
from api.permissions import IsOwnerForUserModel, IsOwner, IsOwnerOrGuest


# For testing purpose only. Have to delete this view in production
class ListUsers(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class DetailUser(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwnerForUserModel,)
    # permission_classes = (IsAuthenticated,)


# For testing purpose only. Have to delete this view in production
class ListUserProfiles(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class DetailUserProfile(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsOwner,)


class ListRooms(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        query = self.request.query_params.get('query', None)
        if query == 'owner':
            return Room.objects.filter(user=user).order_by('-updated_at')
        if query == 'guest':
            return Room.objects.filter(guests=user)
        else:
            return Room.objects.all()

    # def perform_create(self, serializer):
    #     serializer.save(room_owner=self.request.user)


class DetailRoom(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (IsOwnerOrGuest,)


class ListRoomAnswers(generics.ListCreateAPIView):
    queryset = RoomAnswer.objects.all()
    serializer_class = RoomAnswerSerializer


class DetailRoomAnswer(generics.RetrieveUpdateDestroyAPIView):
    queryset = RoomAnswer.objects.all()
    serializer_class = RoomAnswerSerializer


# class UserLogoutAllView(APIView):
#     permission_classes = (IsAuthenticated,)

#     def post(self, request, format=None):
#         user = request.user
#         user.jwt_secret = uuid.uuid4()
#         user.save()
#         return Response(status=status.HTTP_204_NO_CONTENT)
