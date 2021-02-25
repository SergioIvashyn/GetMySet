from import_export import resources

from apps.project.models import Project


class ProjectResource(resources.ModelResource):
    class Meta:
        model = Project
        fields = ('name', 'url', 'description', 'notes', 'is_private')

    def import_row(self, row, *args, **kwargs):
        row_result = super(ProjectResource, self).import_row(row, *args, **kwargs)
        return row_result

    def import_data(self, dataset, *args, **kwargs):
        result = super(ProjectResource, self).import_data(dataset, *args, **kwargs)
        print(result)
        return result
