import uuid

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view

from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode


from core.models import User, Room, Answer
from ..serializers import UserSerializer, SignupSerializer, RoomSerializer, AnswerSerializer
from ..tokens import account_activation_token


class ListUsers(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class DetailUser(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)


class Signup(generics.CreateAPIView):
    serializer_class = SignupSerializer

    def perform_create(self, serializer):
        user = serializer.save()

        current_site = get_current_site(self.request)

        message = render_to_string('email/confirmation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })

        print(message)


"""
        send_mail(
            'Thank you for registration',
            'Here is the message',
            'system.admin@makrub.com',
            ['metz@studiotwist.co'],
            fail_silently=False,
        )
"""


class UserLogoutAllView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        user = request.user
        user.jwt_secret = uuid.uuid4()
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def confirmation(request):
    """
    Confirm user registration
    """

    return Response(status=status.HTTP_200_OK)


class ListRooms(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def perform_create(self, serializer):
        serializer.save(room_owner=self.request.user)


class DetailRoom(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class ListAnswers(generics.ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class DetailAnswer(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
