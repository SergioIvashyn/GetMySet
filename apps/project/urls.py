from django.urls import path, re_path, reverse_lazy
from . import views

urlpatterns = [
    path('projects/private/', views.private_projects, name='private_projects'),
    path('projects/public/', views.public_projects, name='public_projects'),
]