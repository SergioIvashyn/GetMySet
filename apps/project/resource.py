from import_export import resources, widgets
from apps.project.models import Project
from apps.industry.adapter import IndustryFieldToPKModelAdapter
from apps.technology.adapter import TechnologyFieldToPKModelAdapter


class FieldToPKModelWidget(widgets.CharWidget):
    def clean(self, value, row=None, *args, **kwargs):
        val = super().clean(value)
        if val:
            return val
        else:
            raise ValueError('this field is required')


class ProjectResource(resources.ModelResource):
    class Meta:
        model = Project
        fields = ('id', 'name', 'url', 'description', 'notes', 'is_private', 'technologies', 'industries')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ProjectResource, self).__init__()

    def get_user_id(self) -> str:
        return str(self.request.user.id if self.request else '')

    def import_row(self, row, *args, **kwargs):
        new_row = {**row, 'user_id_id': self.get_user_id()}
        row_result = super(ProjectResource, self).import_row(new_row, *args, **kwargs)
        return row_result

    def import_data(self, dataset, *args, **kwargs):
        result = super(ProjectResource, self).import_data(dataset, *args, **kwargs)
        return result
