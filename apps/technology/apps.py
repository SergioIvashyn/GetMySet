from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class TechnologyConfig(AppConfig):
    name = 'apps.technology'
    verbose_name = _('Technologies')
