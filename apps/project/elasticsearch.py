import math
from typing import Optional, List

from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from apps.core.services.elasticsearch_api_base import ElasticSearchModelService, ESPagination
from apps.core import models
from django.utils.translation import gettext_lazy as _


class ProjectElasticSearchModelService(ElasticSearchModelService):
    model = models.Project

    PAGINATION_SIZE = 10

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

    def get_model_body(self, obj: models.Project) -> dict:
        return {
            "name": obj.name,
            "user": obj.user_id,
            "description": obj.description,
            "is_private": obj.is_private,
            "technologies": [elem.name for elem in obj.technologies.all()],
            "industries": [elem.name for elem in obj.industries.all()]
        }

    def filter_projects_context(self, request: WSGIRequest, is_private: bool):
        query_params = request.GET
        page = int(query_params.get('page', 1))
        search = query_params.get('search')
        technologies = query_params.getlist('technologies')
        industries = query_params.getlist('industries')
        user = request.user.pk
        result = self.filter_projects(page=page, search=search, is_private=is_private, user=user,
                                      industries=industries, technologies=technologies)
        return {**result, 'menu': _('Private') if is_private else _('Public')}

    @staticmethod
    def build_unfiltered_aggregation(key: str, filters: list) -> dict:
        return {
            "global": {},
            "aggs": {
                key: {
                    "aggs": {
                        "key": {
                            "terms": {
                                "field": key, "exclude": [""], "size": 10000
                            }
                        }
                    },
                    "filter": {
                        "bool": {
                            "must": filters
                        }
                    }
                }
            }
        }

    @staticmethod
    def get_aggregation_result(filtered_result: List[dict],
                               unfiltered_result: List[dict], searched_entities: List[str]) -> list:
        if not searched_entities:
            return sorted([{**elem, 'is_in_filters': True} for elem in filtered_result], key=lambda x: x.get('key'))
        result = []
        set_searched_entities = frozenset(searched_entities)
        dict_filtered_result = {elem.get('key'): elem.get('doc_count', 0) for elem in filtered_result}
        for elem in unfiltered_result:
            if elem.get('key') in set_searched_entities:
                result.append({**elem, 'is_in_filters': True})
            else:
                key = elem.get('key')
                doc_count = elem.get('doc_count')
                if dict_filtered_result.get(key) and doc_count - dict_filtered_result.get(key, 0) > 0:
                    result.append({'key': key,
                                   'doc_count': doc_count - dict_filtered_result.get(key, 0),
                                   'is_in_filters': False})
        return sorted(result, key=lambda x: x.get('key'))

    def filter_projects(self, page: int = 1, search: Optional[str] = None,
                        user: Optional[int] = None, is_private: Optional[bool] = None,
                        industries: Optional[list] = None, technologies: Optional[list] = None):
        required_query = []
        search_query = []
        industries_aggregation_query = []
        technologies_aggregation_query = []
        if search:
            search_query.append(
                {"multi_match": {"query": search, "type": "phrase_prefix", "fields": ["name", "description"]}})
        if user:
            required_query.append({"term": {"user": user}})
        if industries:
            technologies_aggregation_query.append({"terms": {"industries": industries}})
        if technologies:
            industries_aggregation_query.append({"terms": {"technologies": technologies}})
        if is_private is not None:
            required_query.append({"term": {"is_private": is_private}})

        body = {"query": {"bool": {"must": [*required_query, *search_query, *industries_aggregation_query,
                                            *technologies_aggregation_query]}}}
        documents_count = self._es.count(index=self.model_index, body=body).get('count')
        pagination = ESPagination(size=self.PAGINATION_SIZE, count=documents_count, page=page)
        response = self.search({
            "from": pagination.offset(), "size": self.PAGINATION_SIZE, **body,
            "aggs": {
                "technologies": {"terms": {"field": "technologies", "exclude": [""], "size": 10000}},
                "industries": {"terms": {"field": "industries", "exclude": [""], "size": 10000}},
                "total_count": {"global": {}, "aggs": {"total_count": {"filter": {"bool": {"must": required_query}}}}},
                "unfiltered_technologies": self.build_unfiltered_aggregation(
                    'technologies', [*required_query, *technologies_aggregation_query, *search_query]),
                "unfiltered_industries": self.build_unfiltered_aggregation(
                    'industries', [*required_query, *industries_aggregation_query, *search_query]),
            }
        })
        filtered_industries = response.get('aggregations', {}).get('industries', {}).get('buckets', [])
        unfiltered_industries = response.get('aggregations', {}).get(
            'unfiltered_industries', {}).get('industries', {}).get('key', {}).get('buckets', [])
        filtered_technologies = response.get('aggregations', {}).get('technologies', {}).get('buckets', [])
        unfiltered_technologies = response.get('aggregations', {}).get(
            'unfiltered_technologies', {}).get('technologies', {}).get('key', {}).get('buckets', [])
        return {
            'count': response.get('hits', {}).get('total', {}).get('value', 0),
            'total_count': response.get('aggregations', {}).get('total_count', {}).get('total_count', {}
                                                                                       ).get("doc_count", 0),
            'pagination': pagination, 'qs': self.get_qs_from_search_result(response),
            'technologies': self.get_aggregation_result(filtered_technologies, unfiltered_technologies, technologies),
            'industries': self.get_aggregation_result(filtered_industries, unfiltered_industries, industries),
            'has_filters': any([bool(search), bool(industries), bool(technologies)]),
        }
