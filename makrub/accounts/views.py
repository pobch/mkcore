from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.metadata import BaseMetadata
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
import uuid

from .models import Account
from .serializers import AccountSerializer, SignupSerializer


class ListAccounts(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (AllowAny,)


class DetailAccount(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (IsAuthenticated,)


class Signup(generics.CreateAPIView):
    serializer_class = SignupSerializer


class UserLogoutAllView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        user = request.user
        user.jwt_secret = uuid.uuid4()
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
