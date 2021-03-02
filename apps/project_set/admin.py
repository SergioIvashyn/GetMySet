from apps.core.models.project_set import ProjectSet
from django.contrib import admin

# Register your models here.


@admin.register(ProjectSet)
class ProjectSetAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'url', 'description', 'is_private', 'set', 'is_original']
    ordering = ('id', 'name', )

