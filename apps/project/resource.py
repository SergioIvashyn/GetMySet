from import_export import resources

from apps.project.models import Project


class ProjectResource(resources.ModelResource):

    class Meta:
        model = Project
