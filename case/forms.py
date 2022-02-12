from django.forms import ModelForm
from .models import Case
from django import forms


class CreateCaseForm(ModelForm):
    class Meta:
        model = Case
        exclude = ['owner']
        fields = ['title', 'description', 'contact', 'category',
                  'amount', 'period', 'skill', 'respondent', 'state', 'mode', 'file']

        widgets = {
            'respondent': forms.CheckboxSelectMultiple(),
            'mode': forms.CheckboxSelectMultiple(),
        }
