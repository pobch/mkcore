from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode, base36_to_int

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from core.services import mailer, tokens
from core.models import User

from api import serializers

# django-rest-auth social login:
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView


# django-rest-auth facebook login:
class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class CheckMe(APIView):
    """
    Check whether user auth is working or not
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format="json"):
        return Response("OK")


class Register(APIView):
    """
    Register a new user
    """
    def post(self, request, format='json'):
        serializer = serializers.UserSerializer(data=request.data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()

            confirmation_url = request.build_absolute_uri(reverse('confirmation'))
            token = tokens.user_confirmation_token.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()

            try:
                mailer.send_confirmation_email(user, {
                    'confirmation_url': confirmation_url,
                    'token': token,
                    'uid': uid,
                })
                return Response({'id': user.pk})
            except:
                print('Unexpected errors on sending an e-mail')
                user.delete()
                raise

        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    # def get_serializer(self):
    #     return serializers.UserSerializer()


class Confirmation(APIView):
    """
    Confirm user's email and make that accout activated
    """
    def get(self, request, format='json'):
        uidb64 = self.request.query_params.get('uid')
        token = self.request.query_params.get('token')

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            # ts_b36, hash = token.split("-")
            # ts = base36_to_int(ts_b36)
            # # ts encoded from these command;
            # # from datetime import date
            # # ts = (date.today() - date(2001,1,1)).days - 1
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and tokens.user_confirmation_token.check_token(user, token):
            user.is_active = True
            user.save()

            return Response('Thank you for your email confirmation')
        else:
            return Response('Invalid confirmation link')
