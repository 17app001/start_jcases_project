from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django import forms


class ProfileForm(UserCreationForm):
    class Meta:
        model = Profile
        # 增加email
        fields = ['username', 'email', 'password1',
                  'password2', 'city', 'respondent']

        widgets = {           
            'respondent': forms.RadioSelect(),
        }
