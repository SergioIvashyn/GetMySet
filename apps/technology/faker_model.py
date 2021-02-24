from apps.core.services import FakerModel
from .models import Technology


class TechnologyFakerModel(FakerModel):
    model = Technology
    fake_fields = {'name'}
    CAST_BY_FIELD = {
        'name': 'job',
    }
