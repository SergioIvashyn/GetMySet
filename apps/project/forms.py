from apps.core.models import Project
from django import forms


class ProjectModelForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = forms.ALL_FIELDS

    def save(self, *args, **kwargs):
        instance = super(ProjectModelForm, self).save(*args, **kwargs)
        instance.save(add_to_es=True, refresh=True)
