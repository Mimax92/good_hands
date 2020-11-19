from django.core.mail import EmailMessage
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active)+text_type(user.pk)+text_type(timestamp))


account_activation_token = AppTokenGenerator()
class Util:
    @staticmethod
    def send_email(data):
        email=EmailMessage(subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        email.send()