from django.shortcuts import render

from apps.project.elasticsearch import ProjectElasticSearchModelService

# Create your views here.


def private_projects(request):
    return render(request, 'project/projects.html',
                  ProjectElasticSearchModelService().filter_projects_context(request, is_private=True))


def public_projects(request):
    return render(request, 'project/projects.html',
                  ProjectElasticSearchModelService().filter_projects_context(request, is_private=False))
