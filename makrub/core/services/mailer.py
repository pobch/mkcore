import os
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.conf import settings


def send_confirmation_email(user, options):
    """Send confirmation email after user registration

    Args:
        user (core.User): Newly created user
        options (Dict): options for rendering template
    """
    frontend_domain = os.environ.get('FRONTEND_DOMAIN', 'not_provided_in_env_var')
    confirmation_url = '{}://{}/{}'.format(
            getattr(settings,'PROTOCOL_FOR_ACTIVATION_URL', 'not_provided_in_settings'),
            frontend_domain,
            getattr(settings,'USER_ACTIVATION_CONFIRM_URL', 'not_provided_in_settings')
        )

    app_url = getattr(settings, 'FRONTEND_APP_URL', 'not_provided_in_settings')
    url = "%s/signup/activate/confirm/%s/%s" % (app_url, options['uid'], options['token'])

    # uid.decode('utf-8')

    # message = render_to_string('email/confirmation_email.html', {
    #     'users': user,
    #     'confirmation_url': url,
    # })
    template = get_template('email/confirmation_email.html')
    message = template.render(context={
        'users': user,
        'confirmation_url': url,
    })

    email = EmailMessage('Thank you for registration', message, to=[user.email])
    email.content_subtype = 'html'
    email.send()
