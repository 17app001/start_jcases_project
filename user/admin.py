from django.contrib import admin
from .models import Profile, Respondent, City
from django.contrib.auth.admin import UserAdmin
from .forms import ProfileForm
from .models import Profile

# Register your models here.
# admin.site.register(Profile)
admin.site.register(Respondent)
admin.site.register(City)


class ProfileAdmin(UserAdmin):
    model = Profile
    add_form = ProfileForm
    fieldsets = [
        *UserAdmin.fieldsets,
        [
            'User role',
            {
                'fields': [
                    'point', 'certification', 'city', 'respondent'
                ]
            }
        ]
    ]


admin.site.register(Profile, ProfileAdmin)
