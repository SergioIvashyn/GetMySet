from apps.core.services.field_to_pk_model_adapter import FieldToPKModelAdapter
from apps.industry.models import Industry


class IndustryFieldToPKModelAdapter(FieldToPKModelAdapter):
    model = Industry
