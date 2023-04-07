from django.contrib import admin
from .models import City, Provider, Channel, Incident

admin.site.register(City)
admin.site.register(Provider)
admin.site.register(Channel)
admin.site.register(Incident)

# Register your models here.
