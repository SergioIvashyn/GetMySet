from django.contrib import admin

# Register your models here.
from apps.core.models import UserSet


@admin.register(UserSet)
class UserSetAdmin(admin.ModelAdmin):
    list_display = ['name', 'set_user']
    ordering = ('name', )

