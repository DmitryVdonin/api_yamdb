from django.contrib.auth.tokens import PasswordResetTokenGenerator


class TokenGenerator(PasswordResetTokenGenerator):
    """Генератор токенов для confirmation_code"""
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + str(timestamp)
        )


confirmation_code = TokenGenerator()
