from typing import Type

from django.conf import settings
from django.db.models import Model, QuerySet
from elasticsearch import Elasticsearch
from django.utils.translation import ugettext_lazy as _

elasticsearch = Elasticsearch(hosts=settings.ELASTICSEARCH_URL)


class ElasticSearchModelService:
    model: Type[Model]

    SETTINGS = {
        "number_of_shards": 1,
        "number_of_replicas": 0
    }
    MAPPING = {}

    _PK = 'pk'

    def __init__(self):
        assert self._PK in self.MAPPING.get('properties', {}), _('You don\'t have primary key field into MAPPING. '
                                                                 'Please add it.')
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

    def indexing_model(self, obj: Model) -> 'ElasticSearchModelService':
        self._es.index(index=self.model_index, id=obj.pk, body=self.get_model_body(obj))
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

    def search(self, *args, **kwargs):
        return self._es.search(index=self.model_index, *args, **kwargs)
