from rest_framework import generics

from .models import Account
from .serializers import AccountSerializer


class ListAccounts(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class DetailAccount(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
