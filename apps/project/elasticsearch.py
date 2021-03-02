from apps.core.services.elasticsearch_api_base import ElasticSearchModelService
from apps.project.models import Project


class ProjectElasticSearchModelService(ElasticSearchModelService):
    model = Project

    MAPPING = {
        "properties": {
            "name": {
                "type": "text"
            },
            "description": {
                "type": "text"
            },
            "technologies": {
                "type": 'nested',
                "properties": {
                    "pk": {"type": "integer"},
                    "name": {"type": "text"}
                }
            },
            "industries": {
                "type": 'nested',
                "properties": {
                    "pk": {"type": "integer"},
                    "name": {"type": "text"}
                }
            }
        }
    }

    def get_model_body(self, obj: Project) -> dict:
        return {
            "name": obj.name,
            "description": obj.description,
            "technologies": [{"pk": elem.pk, "name": elem.name} for elem in obj.technologies.all()],
            "industries": [{"pk": elem.pk, "name": elem.name} for elem in obj.industries.all()]
        }
