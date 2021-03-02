from typing import Type, Set, List
from faker import Faker
from django.utils.translation import ugettext_lazy as _

from django.db.models import Model, Field


class FakerModel:
    """Cast Django model class to dict random generated data"""
    __CAST_BY_TYPE = {
        'BooleanField': 'boolean',
        'CharField': 'name',
        'DateField': 'date_object',
        'DateTimeField': 'date_time',
        'DecimalField': 'pydecimal',
        'DurationField': 'time_delta',
        'EmailField': 'email',
        'FloatField': 'pyfloat',
        'IntegerField': 'pyint',
        'BigIntegerField': 'pyint',
        'SmallIntegerField': 'pyint',
        'IPAddressField': 'ipv4',
        'TextField': 'text',
        'URLField': 'url'
    }

    CAST_BY_FIELD: dict = {}

    model: Type[Model]
    fake_fields: Set[str]

    def __init__(self, *args, **kwargs):
        super(FakerModel, self).__init__(*args, **kwargs)
        models_fields = {elem.name for elem in self.model._meta.fields}
        assert len(models_fields.intersection(self.fake_fields)) == len(self.fake_fields), \
            _('Any fields in \"fake_fields\" set does not match with current model fields')
        self._fake = Faker()

    def generate_dict_object(self) -> dict:
        obj = {}
        for field_elem in self.fake_fields:
            if field_elem in self.CAST_BY_FIELD:
                value = getattr(self._fake, self.CAST_BY_FIELD.get(field_elem))()
            else:
                model_field: Field = self.model._meta.get_field(field_elem)
                value = getattr(self._fake, self.__CAST_BY_TYPE.get(
                    model_field.__class__.__name__, 'CharField'))()
            obj[field_elem] = value
        return obj

    def generate_list_of_objects(self, count: int) -> List[dict]:
        return [self.generate_dict_object() for _ in range(count)]

    def save(self):
        obj = self.model.objects.create(**self.generate_dict_object())
        return obj
