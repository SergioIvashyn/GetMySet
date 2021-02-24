from apps.core.services import FakerModel
from .models import Project
from ..industry.models import Industry
from ..technology.models import Technology


class ProjectFakerModel(FakerModel):
    model = Project
    fake_fields = {'name', 'url', 'description', 'is_private'}

    def save(self):
        obj: Project = super(ProjectFakerModel, self).save()
        limit: int = self._fake.random_int(1, 5)
        offset: int = limit + self._fake.random_int(1, 5)
        obj.technologies.set(Technology.objects.order_by('?')[limit:offset])
        obj.industries.set(Industry.objects.order_by('?')[limit:offset])
        return obj
