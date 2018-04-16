from django.contrib.auth.tokens import PasswordResetTokenGenerator


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) +
            str(user.email) +
            str(timestamp) +
            str(user.is_active)
        )


user_confirmation_token = TokenGenerator()
