import math
from typing import Type

from django.conf import settings
from django.db.models import Model, QuerySet
from elasticsearch import Elasticsearch
from django.utils.translation import ugettext_lazy as _

elasticsearch = Elasticsearch(hosts=settings.ELASTICSEARCH_URL)


class ESPagination:

    def __init__(self, count: int, size: int, page: int = 1):
        self._count = count
        self._size = size
        self._page = page

    def page_count(self) -> int:
        return math.ceil(self._count / self._size if self._size != 0 else 1)

    def current_page(self) -> int:
        return self._page

    def page_range(self) -> range:
        return range(1, self.page_count() + 1)

    def has_previous(self) -> bool:
        return self.current_page() > 1

    def has_next(self) -> bool:
        return self.page_count() > self.current_page()

    def offset(self) -> int:
        return self._size * (self._page - 1)

    def next_page_number(self):
        return self._page + 1

    def previous_page_number(self):
        return self._page - 1


class ElasticSearchModelService:
    model: Type[Model]

    SETTINGS = {
        "number_of_shards": 1,
        "number_of_replicas": 0
    }
    MAPPING = {}

    def __init__(self):
        self._es: Elasticsearch = elasticsearch

    @property
    def model_index(self):
        return self.model.__name__.lower()

    def get_index_settings(self):
        return {"settings": self.SETTINGS, "mappings": self.MAPPING}

    def get_query_set(self) -> QuerySet:
        return self.model.objects.all()

    def get_model_body(self, obj: Model) -> dict:
        """Required to implement in child classes"""
        raise NotImplementedError(_('Must implement get_model_body method'))

    def init_model_es_index(self) -> bool:
        exist = self._es.indices.exists(self.model_index)
        if not exist:
            self._es.indices.create(index=self.model_index, body=self.get_index_settings())
        return not exist

    def indexing_model(self, obj: Model, refresh=False) -> 'ElasticSearchModelService':
        self._es.index(index=self.model_index, id=obj.pk, body=self.get_model_body(obj), refresh=refresh)
        return self

    def remove_model_from_index(self, obj: Model) -> 'ElasticSearchModelService':
        self._es.delete(index=self.model_index, id=obj.pk)
        return self

    def fill_index(self) -> None:
        for model_obj in self.get_query_set():
            self.indexing_model(model_obj)

    def clear_index(self) -> None:
        self._es.delete_by_query(index=self.model_index, body={"query": {"match_all": {}}})

    def delete_index(self) -> None:
        self._es.indices.delete(self.model_index)

    def search(self, query) -> dict:
        return self._es.search(index=self.model_index, body=query)

    def get_ids_from_search_result(self, search: dict) -> list:
        return [elem.get('_id') for elem in search.get('hits', {}).get('hits', [])]

    def get_qs_from_search_result(self, search) -> dict:
        return self.model.objects.filter(pk__in=self.get_ids_from_search_result(search))
