from django import forms
from django.forms import widgets

from apps.core.models import Industry


class SearchForm(forms.Form):
    search = forms.CharField(required=False, widget=widgets.TextInput(attrs={'class': 'form-control'}))


class IndustriesForm(forms.Form):
    industries = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'onclick': 'this.form.submit();'}),
    )

    def __init__(self, *args, **kwargs):
        industry_choices = kwargs.pop('industry_choices', ())
        super(IndustriesForm, self).__init__(*args, **kwargs)
        self.fields['industries'].choices = industry_choices
