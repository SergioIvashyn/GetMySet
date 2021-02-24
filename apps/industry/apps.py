from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class IndustryConfig(AppConfig):
    name = 'apps.industry'
    verbose_name = _('Industries')
