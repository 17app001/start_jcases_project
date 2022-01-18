from django.contrib import admin
from .models import Profile, Respondent, City
from django.contrib.auth.admin import UserAdmin
from .forms import ProfileForm

# Register your models here.
admin.site.register(Profile)
admin.site.register(Respondent)
admin.site.register(City)
