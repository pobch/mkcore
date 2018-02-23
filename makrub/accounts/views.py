from rest_framework import generics

from django.contrib.auth.models import User
from .serializers import AccountSerializer


class ListAccounts(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = AccountSerializer


class DetailAccount(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = AccountSerializer
