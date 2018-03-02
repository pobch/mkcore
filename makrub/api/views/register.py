from django.urls import reverse

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from core.services import mailer

from .. import serializers


class Signup(APIView):
    """
    Signup a new user
    """

    def post(self, request, format='json'):
        serializer = serializers.SignupSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            confirmation_url = request.build_absolute_uri(reverse('confirmation'))

            mailer.send_confirmation_email(user, {
                'confirmation_url': confirmation_url,
            })

            return Response({'id': user.pk})

        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def get_serializer(self):
        return serializers.SignupSerializer()


class Confirmation(APIView):
    """
    Confirm user's email and make that accout activated
    """
    def get(self, request, format='json'):
        return Response("OK")
