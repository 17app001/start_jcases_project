from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django import forms


class ProfileForm(UserCreationForm):
    class Meta:
        model = Profile
        # 增加email
        fields = ['username', 'email', 'password1',
                  'password2', 'city', 'respondent']

        labels = {
            'email': '信箱',
            'city': '居住縣市',
            'respondent': '身分',
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.help_text = None

            field.widget.attrs.update(
                {'class': 'input label is-size-5 has-text-centered mt-2 mb-2'}
            )
