from rest_framework_jwt.compat import get_username, get_username_field
from rest_framework_jwt.settings import api_settings
from datetime import datetime
from calendar import timegm


def jwt_otp_payload(user, device=None):
    """
    Put OTP device into JWT payload
    """
    username_field = get_username_field()
    username = get_username(user)

    payload = {
        'user_id': user.pk,
        'username': username,
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
    }

    # include original issued at time for a brand new token, to allow token refresh
    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(datetime.utcnow().utctimetuple())

    if api_settings.JWT_AUDIENCE is not None:
        payload['aud'] = api_settings.JWT_AUDIENCE

    if api_settings.JWT_ISSUER is not None:
        payload['iss'] = api_settings.JWT_ISSUER

    # custom additions
    if (user is not None) and (device is not None) and (device.user_id == user.id) and (device.confirmed is True):
        payload['otp_device_id'] = device.persistent_id # I dont see this field in database naaa !!!!
    else:
        payload['otp_device_id'] = None

    return payload
