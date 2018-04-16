from django.template.loader import render_to_string
from django.core.mail import EmailMessage


def send_confirmation_email(user, options):
    """Send confirmation email after user registration

    Args:
        user (core.User): Newly created user
        options (Dict): options for rendering template
    """
    url = "%s?uid=%s&token=%s" % (options['confirmation_url'], options['uid'], options['token'])
    # uid.decode('utf-8')

    message = render_to_string('email/confirmation_email.html', {
        'users': user,
        'confirmation_url': url,
    })

    email = EmailMessage('Thank you for registration', message, to=[user.email])
    email.send()
