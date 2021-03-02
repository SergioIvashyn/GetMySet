from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ProjectConfig(AppConfig):
    name = 'apps.project'
    verbose_name = _('Projects')

    def ready(self):
        from .signals import es_handle_create_project, es_handle_delete_project
