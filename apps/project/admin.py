from django.contrib import admin
from apps.core.models import Project
from apps.project.resource import ProjectResource
from import_export.admin import ImportExportModelAdmin


# Register your models here.


class ProjectAdmin(ImportExportModelAdmin):
    resource_class = ProjectResource

    def get_resource_kwargs(self, request, *args, **kwargs):
        result = super(ProjectAdmin, self).get_resource_kwargs(request, *args, **kwargs)
        return {**result, 'request': request}


admin.site.register(Project, ProjectAdmin)
