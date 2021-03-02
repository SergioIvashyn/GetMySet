from apps.core.services.elasticsearch_api_base import ElasticSearchModelService
from apps.project.models import Project


class ProjectElasticSearchModelService(ElasticSearchModelService):
    model = Project

    MAPPING = {
        "properties": {
            "name": {
                "type": 'text'
            },
            "description": {
                "type": 'text'
            }
        }
    }
