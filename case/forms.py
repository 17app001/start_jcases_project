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

    def __init__(self, *args, **kwargs):
        super(CreateCaseForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.help_text = None

            if name in ['category', 'amount', 'period', 'state']:
                field.widget.attrs.update(
                    {'class': 'select is-size-5 mb-2'})
            elif name == 'description':
                field.widget.attrs.update(
                    {'class': 'textarea is-size-6 mb-2'})
            elif name in ['respondent', 'mode']:
                field.widget.attrs.update(
                    {'class': 'checkbox is-size-5 mb-2'})
            else:
                field.widget.attrs.update(
                    {'class': 'input label is-size-5 has-text-centered mt-2 mb-2'}
                )
