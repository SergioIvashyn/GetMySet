from django.contrib import admin
from apps.core.models.technology import Technology


# Register your models here.


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)
