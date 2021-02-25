from apps.core.services.field_to_pk_model_adapter import FieldToPKModelAdapter
from apps.technology.models import Technology


class TechnologyFieldToPKModelAdapter(FieldToPKModelAdapter):
    model = Technology
    default_field = 'name'
