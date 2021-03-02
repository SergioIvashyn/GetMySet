from dataclasses import dataclass
from typing import Type, List

from django.db.models import Model


@dataclass
class FieldToPKModelAdapter:
    """Adapted array of field model to array of object pk"""

    model: Type[Model]
    array: List[str]
    field: str = ''

    @classmethod
    def create_from_string(cls, model: Type[Model], string: str, field: str = '', separator: str = ','):
        return cls(model, list(map(lambda x: x.strip().title(), string.split(separator))), field)

    def adapted(self) -> list:
        new_array = []
        for value in self.array:
            obj, _ = self.model.objects.get_or_create(**{self.field: value})
            new_array.append(str(obj.pk))
        return new_array

    def adapted_to_string(self, separator: str = ',') -> str:
        return separator.join(self.adapted())
