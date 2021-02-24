from django.contrib import admin

# Register your models here.
from apps.company.models import Company

admin.site.register(Company)
