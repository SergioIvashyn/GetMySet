from django.contrib import admin
from django import forms
from django.forms import ValidationError
from import_export.formats.base_formats import CSV
from import_export.forms import ImportForm, ConfirmImportForm
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User
from apps.core.models import Project
from apps.project.resource import ProjectResource
from import_export.admin import ImportExportModelAdmin


# Register your models here.

class ProjectImportForm(ImportForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_import_file(self):
        if self.cleaned_data['import_file'].content_type not in {'application/vnd.ms-excel', 'text/csv'}:
            raise ValidationError(_('Current file is not CSV'))
        return self.cleaned_data['import_file']

    def clean(self):
        cleaned_data = super(ProjectImportForm, self).clean()
        # print(self.cleaned_data['import_file'].name)
        # print(dir(self.cleaned_data['import_file']))
        return cleaned_data


class ProjectConfirmImportForm(ConfirmImportForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput(), required=False)


class ProjectAdmin(ImportExportModelAdmin):
    resource_class = ProjectResource
    from_encoding = "utf-8"
    formats = (CSV,)
    import_template_name = 'import_export.html'

    def get_resource_kwargs(self, request, *args, **kwargs):
        result = super(ProjectAdmin, self).get_resource_kwargs(request, *args, **kwargs)
        return {**result, **kwargs, 'request': request}

    def get_import_form(self):
        return ProjectImportForm

    def get_confirm_import_form(self):
        return ProjectConfirmImportForm

    def get_form_kwargs(self, form, *args, **kwargs):
        if isinstance(form, ProjectImportForm):
            kwargs['user'] = form.cleaned_data.get('user', None)
        return kwargs


admin.site.register(Project, ProjectAdmin)
