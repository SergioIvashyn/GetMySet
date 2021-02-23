from dataclasses import dataclass
from django.utils.translation import ugettext_lazy as _

from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from demo.settings import DEFAULT_FROM_EMAIL


@dataclass
class UserEmailSender:
    user_email: str

    def send_activation_message(self) -> 'UserEmailSender':
        return self._send_email(context={'email': self.user_email},
                                subject=_('Account activation'), template='accounts/email/activation_message.html')

    def _send_email(self, context: dict, subject: str, template: str) -> 'UserEmailSender':
        html_message = render_to_string(template, context)
        plain_message = strip_tags(html_message)
        try:
            mail.send_mail(subject, plain_message, DEFAULT_FROM_EMAIL, [self.user_email], html_message=html_message,
                           fail_silently=False)
        except Exception as e:
            print(e)
        return self
