from typing import Optional

from import_export import resources, fields

from apps.core.models import Technology, Project, Industry
from apps.core.services.import_export_widget import FieldToPKManyToManyWidget


class ProjectResource(resources.ModelResource):
    technologies = fields.Field(column_name='technologies', attribute='technologies',
                                widget=FieldToPKManyToManyWidget(Technology, field='name'))
    industries = fields.Field(column_name='industries', attribute='industries',
                              widget=FieldToPKManyToManyWidget(Industry, field='name'))

    class Meta:
        model = Project
        fields = ('name', 'url', 'description', 'notes', 'is_private', 'technologies', 'industries')
        import_id_fields = ('name', 'user_id')
        clean_model_instances = True

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.cleaned_data = getattr(kwargs.pop('form', None), 'cleaned_data', {})
        super(ProjectResource, self).__init__()

    def get_or_init_instance(self, instance_loader, row):
        self.fields['user_id'] = fields.Field(attribute='user_id', column_name='user_id')
        row['user_id'] = self.get_user_id()
        return super(ProjectResource, self).get_or_init_instance(instance_loader, row)

    def get_user_id(self) -> Optional[int]:
        return getattr(self.cleaned_data.get('user'), 'id', None) or (self.request.user.id if self.request else None)
