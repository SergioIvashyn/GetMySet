import math
from typing import Optional, OrderedDict

from django.db.models import QuerySet
from apps.core.services.elasticsearch_api_base import ElasticSearchModelService, ESPagination
from apps.core.models import Project


class ProjectElasticSearchModelService(ElasticSearchModelService):
    model = Project

    PAGINATION_SIZE = 3

    MAPPING = {
        "properties": {
            "name": {
                "type": "text"
            },
            "user": {
                "type": "integer"
            },
            "description": {
                "type": "text"
            },
            "technologies": {
                "type": 'keyword'
            },
            "industries": {
                "type": 'keyword'
            },
            "is_private": {
                "type": "boolean"
            }
        }
    }

    def get_query_set(self) -> QuerySet:
        return self.model.objects.all().prefetch_related('technologies').prefetch_related('industries')

    def get_model_body(self, obj: Project) -> dict:
        return {
            "name": obj.name,
            "user": obj.user_id,
            "description": obj.description,
            "is_private": obj.is_private,
            "technologies": [elem.name for elem in obj.technologies.all()],
            "industries": [elem.name for elem in obj.industries.all()]
        }

    def filter_projects_context(self, request, is_private: bool):
        query_params: OrderedDict = request.GET
        page = int(query_params.get('page', 1))
        search = query_params.get('search')
        technologies = query_params.get('technologies')
        industries = query_params.get('industries')
        user = request.user.pk
        result = self.filter_projects(page=page, search=search, is_private=is_private, user=user,
                                      industries=industries, technologies=technologies)
        return result

    def filter_projects(self, page: int = 1, search: Optional[str] = None,
                        user: Optional[int] = None, is_private: Optional[bool] = None,
                        industries: Optional[list] = None, technologies: Optional[list] = None):
        size = self.PAGINATION_SIZE
        query = []
        if search:
            query.append({"query_string": {"query": search, "fields": ["name", "description"]}})
        if user:
            query.append({"term": {"user": user}})
        if industries:
            query.append({"term": {"industries": industries}})
        if is_private is not None:
            query.append({"term": {"is_private": is_private}})
        if technologies:
            query.append({"term": {"technologies": technologies}})
        body = {"query": {"bool": {"must": query}}}
        total_count = self._es.count(index=self.model_index, body=body).get('count')
        pagination = ESPagination(size=size, count=total_count, page=page)

        response = self.search({
            "from": pagination.offset(), "size": size,
            **body,
            "aggs": {
                "technologies": {"terms": {"field": "technologies", "exclude": [""]}},
                "industries": {"terms": {"field": "industries", "exclude": [""]}}
            }
        })
        return {
            'count': response.get('hits', {}).get('total', {}).get('value', 0),
            'total_count': total_count,
            'pagination': pagination,
            'qs': self.get_qs_from_search_result(response),
            'technologies': sorted(response.get('aggregations', {}).get('technologies', {}).get('buckets', []),
                                   key=lambda x: x.get('key')),
            'industries': sorted(response.get('aggregations', {}).get('industries', {}).get('buckets', []),
                                 key=lambda x: x.get('key')),
            'has_filters': any([bool(search), bool(industries), bool(technologies)]),
        }
