from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from core.services import mailer
from core.tokens import user_confirmation_token
from core.models import User

from api import serializers


class Signup(APIView):
    """
    Signup a new user
    """

    def post(self, request, format='json'):
        serializer = serializers.SignupSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()

            confirmation_url = request.build_absolute_uri(reverse('confirmation'))
            token = user_confirmation_token.make_token(user)

            mailer.send_confirmation_email(user, {
                'confirmation_url': confirmation_url,
                'token': token,
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
        uidb64 = request.GET.get('uid')
        token = request.GET.get('token')

        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and user_confirmation_token.check_token(user, token):
            user.is_active = True
            user.save()

            return Response('Thank you for your email confirmation')
        else:
            return Response('Invalid confirmation link')
