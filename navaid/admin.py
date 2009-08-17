from django.contrib.gis import admin
from models import Navaid

class NavaidAdmin(admin.GeoModelAdmin):
    list_display = ('identifier', 'name', 'type',)
    search_fields = ('identifier', 'name',)

admin.site.register(Navaid, NavaidAdmin)
