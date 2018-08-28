import requests
import facebook
import sys

from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode, base36_to_int
from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework_jwt.settings import api_settings

from core.services import mailer, tokens

from api import serializers

User = get_user_model()

class CheckMe(APIView):
    """
    Check whether user auth is working or not
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format="json"):
        return Response("OK")

class Facebook(APIView):
    """
    Authenticate via facebook
    """
    def get(self, request):
        code = request.GET.get('code')

        if not code:
            return Response(status = 400)

        params = {
            'code': code,
            'client_id': getattr(settings, 'FACEBOOK_APP_ID'),
            'client_secret': getattr(settings, 'FACEBOOK_APP_SECRET'),
            'redirect_uri': getattr(settings, 'FACEBOOK_REDIRECT_URI'),
        }

        r = requests.get('https://graph.facebook.com/v3.1/oauth/access_token', params=params)
        data = r.json()

        if 'error' in data:
            return Response(data["error"], status=422)

        graph = facebook.GraphAPI(access_token=data["access_token"], version="3.0")
        me = graph.get_object(id="me", fields="email,first_name,last_name")

        try:
            user = User.objects.get(email = me["email"])
            return Response({
                'id': user.pk,
                'email': user.email,
                'token': generate_jwt_token(user)
            })
        except User.DoesNotExist:
            user = User()
            user.email = me["email"]
            user.first_name = me["first_name"]
            user.last_name = me["last_name"]
            user.is_active = True

            user.save()

            result = confirm_user(user)

            if result:
                return Response({
                    'id': user.pk,
                    'email': user.email,
                    'token': generate_jwt_token(user)
                })
            else:
                print("result failed")
                return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class Register(APIView):
    """
    Register a new user
    """
    def post(self, request, format='json'):
        serializer = serializers.UserSerializer(data=request.data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()

            # confirmation_url = request.build_absolute_uri(reverse('confirmation'))
            token = tokens.user_confirmation_token.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()

            try:
                mailer.send_confirmation_email(user, {
                    # 'confirmation_url': confirmation_url,
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
            return Response('Invalid confirmation link', status=status.HTTP_400_BAD_REQUEST)

"""
confirm_user

helper function for sending a confirmation e-mail to user
"""
def confirm_user(user):
    token = tokens.user_confirmation_token.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()

    try:
        mailer.send_confirmation_email(user, {
            # 'confirmation_url': confirmation_url,
            'token': token,
            'uid': uid,
        })

        return True
    except:
        print('Unexpected errors on sending an e-mail', sys.exc_info()[0])

        return False

"""
generate_jwt_token

helper function for generate jwt token for given user
"""
def generate_jwt_token(user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)

    return token
