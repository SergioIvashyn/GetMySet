from apps.core.models.industry import Industry
from django.contrib import admin

# Register your models here.


@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    ordering = ('id', 'name',)
