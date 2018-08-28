import requests
import facebook

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

        app_id = getattr(settings, 'FACEBOOK_APP_ID')
        app_secret = getattr(settings, 'FACEBOOK_APP_SECRET')

        params = {
            'client_id': app_id,
            'client_secret': app_secret,
            'code': code,
            'redirect_uri': 'https://localhost:3000/app/auth/facebook',
        }

        r = requests.get('https://graph.facebook.com/v3.1/oauth/access_token', params=params)
        data = r.json()

        if 'error' in data:
            return Response(data["error"], status=422)
        try:
            user = User.objects.get(email = "methsg@gmail.com")
        except User.DoesNotExist:
            graph = facebook.GraphAPI(access_token=data["access_token"], version="3.0")
            me = graph.get_object(id="me", fields="email,first_name,last_name")

            user = User()
            user.email = me["email"]
            user.first_name = me["first_name"]
            user.last_name = me["last_name"]

            user.save()
            pass

        print(user)

        return Response("OK")


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
