from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SetConfig(AppConfig):
    name = 'apps.set'
    verbose_name = _('Sets')
