from apps.core.services import FakerModel
from apps.core.models import Industry


class IndustryFakerModel(FakerModel):
    model = Industry
    fake_fields = {'name'}
    CAST_BY_FIELD = {
        'name': 'company',
    }
