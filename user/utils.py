from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class TokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return six.text_type(str(user.id))+six.text_type(str(timestamp))\
            + six.text_type(user.certification)


generator_token = TokenGenerator()