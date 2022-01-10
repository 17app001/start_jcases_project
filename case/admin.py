from django.contrib import admin
from .models import City,Category,Amount,Mode,State,Respondent,Period

# Register your models here.
admin.site.register(City)
admin.site.register(Category)
admin.site.register(Amount)
admin.site.register(Mode)
admin.site.register(State)
admin.site.register(Respondent)
admin.site.register(Period)

