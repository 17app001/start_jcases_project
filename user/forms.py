from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Profile
from django import forms


class UpdateProfileForm(ModelForm):
    class Meta:
        model = Profile
        # 增加email       
        fields = ['email','respondent', 'person_image']

        labels = {
            'email': '信箱',
            'respondent': '身分',
            'person_image': '照片(default)',
        }

    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.help_text = None
            field.widget.attrs.update(
                {'class': 'input label is-size-5 has-text-centered mt-2 mb-2'}
            )

class ProfileForm(UserCreationForm):
    class Meta:
        model = Profile
        # 增加email
        fields = ['username', 'email', 'password1',
                  'password2', 'city', 'respondent', 'person_image']

        labels = {
            'email': '信箱',
            'city': '居住縣市',
            'respondent': '身分',
            'person_image': '照片(default)',
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.help_text = None
            field.widget.attrs.update(
                {'class': 'input label is-size-5 has-text-centered mt-2 mb-2'}
            )
