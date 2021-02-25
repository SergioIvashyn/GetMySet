from django.contrib import admin

# Register your models here.
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST

from apps.project.models import Project
from apps.project.resource import ProjectResource
from import_export.admin import ImportExportModelAdmin


class ProjectAdmin(ImportExportModelAdmin):
    resource_class = ProjectResource

    def get_resource_kwargs(self, request, *args, **kwargs):
        result = super(ProjectAdmin, self).get_resource_kwargs(request, *args, **kwargs)
        return {**result, 'request': request}


admin.site.register(Project, ProjectAdmin)
