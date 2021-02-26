from typing import Optional

from import_export import resources, widgets, fields
from import_export.instance_loaders import ModelInstanceLoader
from import_export.widgets import Widget

from apps.core.services.import_export_widget import FieldToPKManyToManyWidget
from apps.industry.models import Industry
from apps.project.models import Project
from apps.technology.models import Technology


class ProjectResource(resources.ModelResource):
    technologies = fields.Field(column_name='technologies', attribute='technologies',
                                widget=FieldToPKManyToManyWidget(Technology, field='name'))
    industries = fields.Field(column_name='industries', attribute='industries',
                              widget=FieldToPKManyToManyWidget(Industry, field='name'))

    class Meta:
        model = Project
        fields = ('name', 'url', 'description', 'notes', 'is_private', 'technologies', 'industries')
        import_id_fields = ('name', 'user_id_id')
        clean_model_instances = True

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ProjectResource, self).__init__()
        self.fields['user_id_id'] = fields.Field(attribute='user_id_id', column_name='user_id_id')

    def get_or_init_instance(self, instance_loader, row):
        row['user_id_id'] = self.get_user_id()
        return super(ProjectResource, self).get_or_init_instance(instance_loader, row)

    def get_user_id(self) -> Optional[int]:
        return self.request.user.id if self.request else None
