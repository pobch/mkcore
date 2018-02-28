from rest_framework.views import APIView
from rest_framework.response import Response

from .. import serializers


class Signup(APIView):
    """
    Signup a new user
    """

    def post(self, request, format='json'):
        return Response("hello")

    def get_serializer(self):
        return serializers.SignupSerializer()
