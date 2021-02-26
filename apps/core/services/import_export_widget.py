from typing import Type

from apps.core.services.field_to_pk_model_adapter import FieldToPKModelAdapter

from import_export import widgets


class FieldToPKManyToManyWidget(widgets.ManyToManyWidget):

    def __init__(self, *args, **kwargs):
        self.adapter: Type[FieldToPKModelAdapter] = FieldToPKModelAdapter
        super(FieldToPKManyToManyWidget, self).__init__(*args, **kwargs)

    def clean(self, value, row=None, *args, **kwargs):
        if not value:
            return self.model.objects.none()
        if isinstance(value, (float, int)):
            ids = [int(value)]
        else:
            ids = self.adapter.create_from_string(self.model, value, self.field, self.separator).adapted()
            ids = filter(None, [i.strip() for i in ids])
        return self.model.objects.filter(**{'id__in': ids})
