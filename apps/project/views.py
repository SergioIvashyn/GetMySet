from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView

from apps.core.models import Project
from apps.project.elasticsearch import ProjectElasticSearchModelService
from apps.project.forms import ProjectModelForm

from django.core.handlers.wsgi import WSGIRequest
# Create your views here.


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
