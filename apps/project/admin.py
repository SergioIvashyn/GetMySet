from django.contrib import admin

# Register your models here.
from apps.core.models.project import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'url', 'description', 'is_private']
    ordering = ('id', 'name', )

