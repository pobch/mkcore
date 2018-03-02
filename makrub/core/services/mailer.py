from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from core.tokens import user_confirmation_token


def send_confirmation_email(user, options):
    """Send confirmation email after user registration

    Args:
        user (core.User): Newly created user
        options (Dict): options for rendering template
    """
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = user_confirmation_token.make_token(user)

    url = "%s?uid=%s&token=%s" % (options['confirmation_url'], uid.decode('utf-8'), token)

    message = render_to_string('email/confirmation_email.html', {
        'users': user,
        'confirmation_url': url,
    })

    email = EmailMessage('Thank you for registration', message, to=[user.email])
    email.send()
