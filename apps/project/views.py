from apps.core.models.industry import Industry
from apps.core.models.project import Project
from apps.core.models.technology import Technology

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render


# Create your views here.


def private_projects(request):
    industries = Industry.objects.project_page_qs(request)
    technologies = Technology.objects.project_page_qs(request)
    page_number = request.GET.get('page', 1)
    qs = Project.objects.private(request)
    paginator = Paginator(qs, 3)
    try:
        page_obj = paginator.page(page_number)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, 'project/projects.html',
                  {'qs': page_obj, 'industries': industries, 'technologies': technologies})


def public_projects(request):
    industries = Industry.objects.project_page_qs(request)
    technologies = Technology.objects.project_page_qs(request)
    page_number = request.GET.get('page', 1)
    qs = Project.objects.public(request)
    paginator = Paginator(qs, 3)
    try:
        page_obj = paginator.page(page_number)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, 'project/projects.html',
                  {'qs': page_obj, 'industries': industries, 'technologies': technologies})
