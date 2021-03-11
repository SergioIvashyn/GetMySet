from django.urls import path, re_path, reverse_lazy
from . import views, signals

urlpatterns = [
    path('projects/private/', views.private_projects, name='private_projects'),
    path('projects/public/', views.public_projects, name='public_projects'),
    path('projects/import/', views.ProjectImportView.as_view(), name='import_projects'),
]
