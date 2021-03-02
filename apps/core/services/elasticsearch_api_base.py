from typing import Type

from django.conf import settings
from django.db.models import Model
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

    def __init__(self):
        self.es: Elasticsearch = elasticsearch

    @property
    def model_index(self):
        return self.model.__name__.lower()

    def get_index_settings(self):
        return {"settings": self.SETTINGS, "mappings": self.MAPPING}

    def init_model_es_index(self) -> bool:
        exist = self.es.indices.exists(self.model_index)
        if not exist:
            self.es.indices.create(index=self.model_index, body=self.get_index_settings())
        return not exist

    def get_model_body(self, obj: Model) -> dict:
        """Required to implement in child classes"""
        raise NotImplementedError(_('Must implement get_model_body method'))

    def indexing_model(self, obj: Model) -> 'ElasticSearchModelService':
        self.es.index(index=self.model_index, id=obj.pk, body=self.get_model_body(obj))
        return self

    def remove_model_from_index(self, obj: Model) -> 'ElasticSearchModelService':
        self.es.delete(index=self.model_index, id=obj.pk)
        return self

    def fill_index(self):
        for model_obj in self.model.objects.all():
            self.indexing_model(model_obj)
