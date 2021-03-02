from django.contrib import admin

# Register your models here.
from apps.core.models import UserSet


@admin.register(UserSet)
class UserSetAdmin(admin.ModelAdmin):
    fields = ['id', 'name', 'set_user']
    list_display = ['id', 'name', 'set_user']
    ordering = ('name', )

