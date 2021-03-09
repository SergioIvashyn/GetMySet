from django.contrib import admin
from django import forms
from django.core.exceptions import PermissionDenied
from django.forms import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from import_export.formats.base_formats import CSV, XLS
from import_export.forms import ImportForm, ConfirmImportForm, ExportForm
from django.utils.translation import gettext_lazy as _
from import_export.signals import post_export

from apps.accounts.models import User
from apps.core.models import Project
from apps.project.resource import ProjectResource
from import_export.admin import ImportExportModelAdmin


# Register your models here.

class ProjectExportForm(ExportForm):
    user = forms.ModelChoiceField(queryset=User.objects.all())


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
    formats = (CSV, XLS, )
    import_template_name = 'import_export.html'
    list_display = ('name', 'url', 'is_private', 'user')
    actions = [
        'export_admin_action_as_csv',
        'export_admin_action_as_xls'
    ]

    def _export(self, request, queryset, file_format):
        export_data = self.get_export_data(file_format, queryset, request=request)
        content_type = file_format.get_content_type()
        response = HttpResponse(export_data, content_type=content_type)
        response['Content-Disposition'] = 'attachment; filename="%s"' % (
            self.get_export_filename(request, queryset, file_format),
        )
        return response

    def export_admin_action_as_csv(self, request, queryset):
        file_format = CSV()
        return self._export(request, queryset, file_format)

    export_admin_action_as_csv.short_description = _(
        'Export selected %(verbose_name_plural)s as CSV')

    def export_admin_action_as_xls(self, request, queryset):
        file_format = XLS()
        return self._export(request, queryset, file_format)

    export_admin_action_as_xls.short_description = _(
        'Export selected %(verbose_name_plural)s as XLS')

    def export_action(self, request, *args, **kwargs):
        if not self.has_export_permission(request):
            raise PermissionDenied

        formats = self.get_export_formats()
        form = ProjectExportForm(formats, request.POST or None)
        if form.is_valid():
            file_format = formats[
                int(form.cleaned_data['file_format'])
            ]()
            user = form.cleaned_data['user']
            queryset = self.get_export_queryset(request).filter(user=user)
            export_data = self.get_export_data(file_format, queryset, request=request)
            content_type = file_format.get_content_type()
            response = HttpResponse(export_data, content_type=content_type)
            response['Content-Disposition'] = 'attachment; filename="%s"' % (
                self.get_export_filename(request, queryset, file_format),
            )

            post_export.send(sender=None, model=self.model)
            return response

        context = self.get_export_context_data()

        context.update(self.admin_site.each_context(request))

        context['title'] = _("Export")
        context['form'] = form
        context['opts'] = self.model._meta
        request.current_app = self.admin_site.name
        return TemplateResponse(request, [self.export_template_name],
                                context)

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

    def save_model(self, request, obj, form, change):
        obj.save(add_to_es=True, refresh=True)


admin.site.register(Project, ProjectAdmin)
