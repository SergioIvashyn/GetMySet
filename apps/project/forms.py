from django.core.exceptions import ValidationError
from import_export.forms import ImportForm
from django.utils.translation import gettext_lazy as _

from apps.core.models import Project
from django import forms


class ProjectModelForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'url', 'user', 'description', 'notes', 'is_private', 'technologies', 'industries']

    def save(self, *args, **kwargs):
        instance = super(ProjectModelForm, self).save(*args, **kwargs)
        instance.save(add_to_es=True, refresh=True)


class ProjectImportForm(ImportForm):
    import_file = forms.FileField(label='')
    input_format = forms.ChoiceField(label=_('Format'), choices=(),
                                     widget=forms.Select(attrs={'class': "form-control"}))

    def clean_import_file(self):
        if self.cleaned_data['import_file'].content_type not in {'application/vnd.ms-excel', 'text/csv'}:
            raise ValidationError(_('Current file is not valid CSV\\XLS file'))
        return self.cleaned_data['import_file']
