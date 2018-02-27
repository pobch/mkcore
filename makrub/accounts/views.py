from rest_framework import generics
from rest_framework.response import Response

from .models import Account
from .serializers import AccountSerializer, SignupSerializer, LoginSerializer


class ListAccounts(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class DetailAccount(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class Signup(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = SignupSerializer


class Login(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            return Response("OK")

        return Response("NOT OK")
