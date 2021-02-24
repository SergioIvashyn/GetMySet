from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ProjectConfig(AppConfig):
    name = 'apps.project'
    verbose_name = _('Projects')
