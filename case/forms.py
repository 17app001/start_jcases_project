from django.forms import ModelForm
from .models import Case


class CreateCaseForm(ModelForm):
    class Meta:
        model = Case
        exclude = ['owner']
        fields = ['title', 'description', 'contact', 'category',
                  'amount', 'period', 'skill', 'respondent', 'state', 'mode']
