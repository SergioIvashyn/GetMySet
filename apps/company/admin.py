from django.contrib import admin

# Register your models here.
from apps.core.models.company import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    fields = ['id', 'name', 'site_url']
    list_display = ['id', 'name', 'site_url']
    ordering = ('name', )
