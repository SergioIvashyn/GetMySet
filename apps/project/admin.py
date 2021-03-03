from django.contrib import admin
from django import forms
from import_export.forms import ImportForm, ConfirmImportForm

from apps.accounts.models import User
from apps.core.models import Project
from apps.project.resource import ProjectResource
from import_export.admin import ImportExportModelAdmin


# Register your models here.

class ProjectImportForm(ImportForm):
    user = forms.ModelChoiceField(queryset=User.objects.all())


class ProjectConfirmImportForm(ConfirmImportForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(ProjectConfirmImportForm, self).__init__(*args, **kwargs)


class ProjectAdmin(ImportExportModelAdmin):
    resource_class = ProjectResource

    def get_resource_kwargs(self, request, *args, **kwargs):
        result = super(ProjectAdmin, self).get_resource_kwargs(request, *args, **kwargs)
        return {**result, **kwargs}

    def get_import_form(self):
        return ProjectImportForm

    def get_confirm_import_form(self):
        return ProjectConfirmImportForm

    def get_form_kwargs(self, form, *args, **kwargs):
        if isinstance(form, ProjectImportForm):
            kwargs['user'] = form.cleaned_data.get('user', None)
        return kwargs


admin.site.register(Project, ProjectAdmin)
