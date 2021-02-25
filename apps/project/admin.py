from django.contrib import admin

# Register your models here.
from apps.project.models import Project
from apps.project.resource import ProjectResource
from import_export.admin import ImportExportModelAdmin


class ProjectAdmin(ImportExportModelAdmin):
    resource_class = ProjectResource


admin.site.register(Project, ProjectAdmin)
