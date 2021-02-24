from django.contrib import admin

# Register your models here.
from apps.project.models import Project

admin.site.register(Project)
