from typing import Type, List

from django.db.models import Model
from django.utils.translation import ugettext_lazy as _


class FieldToPKModelAdapter:
    """Adapted array of field model to array of object pk"""
    model: Type[Model]
    default_field: str

    @classmethod
    def create_from_string(cls, string: str, field: str = '', separator: str = ','):
        return cls(list(map(lambda x: x.title(), string.split(separator))), field)

    def __init__(self, array: List[str], field: str = ''):
        assert bool(self.default_field), _('default_field is required')
        self.field = self.field if self.field else self.default_field
        self.array: list = array
        self.field: str = field

    def adapted(self) -> list:
        new_array = []
        for value in self.array:
            obj, _ = self.model.objects.get_or_create(**{self.field: value})
            new_array.append(str(obj.pk))
        return new_array

    def adapted_to_string(self, separator: str = ','):
        return separator.join(self.adapted())
