from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.encoding import force_str
from django.views import View
from django.views.generic import CreateView
from import_export.admin import ImportMixin
from import_export.formats.base_formats import CSV, XLS
from import_export.forms import ImportForm
from tablib import Dataset
from django.utils.translation import gettext_lazy as _

from apps.core.models import Project
from apps.project.elasticsearch import ProjectElasticSearchModelService
from apps.project.forms import ProjectModelForm, ProjectImportForm

from django.core.handlers.wsgi import WSGIRequest
# Create your views here.
from apps.project.resource import ProjectResource
from apps.project.tasks import save_projects_from_csv


def private_projects(request: WSGIRequest):
    return render(request, 'project/projects.html',
                  ProjectElasticSearchModelService().filter_projects_context(request, is_private=True))


def public_projects(request):
    return render(request, 'project/projects.html',
                  ProjectElasticSearchModelService().filter_projects_context(request, is_private=False))


class ProjectCreateView(LoginRequiredMixin, CreateView):
    template_name = 'app/create.html'
    model = Project
    form_class = ProjectModelForm

    def get_success_url(self):
        return reverse('app:detail')


class ProjectImportView(LoginRequiredMixin, ImportMixin, View):
    template = 'project/import_csv.html'
    resource_class = ProjectResource
    formats = (CSV, XLS)

    def get(self, request):
        form = self.get_import_form()(import_formats=self.get_import_formats())
        return render(request, self.template, {'form': form})

    def get_import_form(self):
        return ProjectImportForm

    def post(self, request):
        form = self.get_import_form()(data=request.POST, files=request.FILES, import_formats=self.get_import_formats())
        if form.is_valid():
            import_formats = self.get_import_formats()
            input_format_int = int(form.cleaned_data['input_format'])
            input_format = import_formats[input_format_int]()
            import_file = form.cleaned_data['import_file']
            tmp_storage = self.write_to_tmp_storage(import_file, input_format)
            try:
                data = tmp_storage.read(input_format.get_read_mode())
                if not input_format.is_binary() and self.from_encoding:
                    data = force_str(data, self.from_encoding)
                save_projects_from_csv.delay(data, request.user.id, input_format_int)
            except Exception as e:
                return JsonResponse({'error': True, 'errors': [
                    f'{_("Current file is not ")}{input_format.__class__.__name__}']})
            # messages.success(request, _('Import finished, with %(new)d new and %(update)d updated Projects.') %
            #                  result.totals)
            return JsonResponse({'error': False})
        else:
            return JsonResponse({'error': True, 'errors': form.errors})
