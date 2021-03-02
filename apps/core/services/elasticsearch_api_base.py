from typing import Type

from django.conf import settings
from django.db.models import Model
from elasticsearch import Elasticsearch

elasticsearch = Elasticsearch(hosts=settings.ELASTICSEARCH_URL)


class ElasticSearchModelService:
    model: Type[Model]
    SETTINGS = {
        "number_of_shards": 1,
        "number_of_replicas": 0
    }
    MAPPING = {}

    def __init__(self):
        self.elasticsearch = elasticsearch

    @property
    def model_index(self):
        return self.model.__name__.lower()

    def get_model_body(self, obj: Model) -> dict:
        """Required to implement in child classes"""
        pass

    def indexing_model(self, obj: Model) -> 'ElasticSearchModelService':
        self.elasticsearch.index(index=self.model_index, id=obj.pk, body=self.get_model_body(obj))
        return self

    def update_index(self, obj: Model) -> 'ElasticSearchModelService':
        return self

    def delete_index(self, obj: Model) -> 'ElasticSearchModelService':
        self.elasticsearch.delete(index=self.model_index, id=obj.pk)
        return self
