from django.db.models import QuerySet

from apps.core.services.elasticsearch_api_base import ElasticSearchModelService
from apps.core.models import Project


class ProjectElasticSearchModelService(ElasticSearchModelService):
    model = Project

    MAPPING = {
        "properties": {
            "pk": {
                "type": "integer"
            },
            "name": {
                "type": "text"
            },
            "description": {
                "type": "text"
            },
            "technologies": {
                "type": 'keyword'
            },
            "industries": {
                "type": 'keyword'
            }
        }
    }

    def get_query_set(self) -> QuerySet:
        return self.model.objects.all().prefetch_related('technologies').prefetch_related('industries')

    def get_model_body(self, obj: Project) -> dict:
        return {
            "name": obj.name,
            "description": obj.description,
            "technologies": [elem.name for elem in obj.technologies.all()],
            "industries": [elem.name for elem in obj.industries.all()]
        }
