from django.contrib.gis import admin
from models import Navaid

class NavaidAdmin(admin.GeoModelAdmin):
    list_display = ('identifier', 'name', 'municipality',)
    search_fields = ('identifier', 'name', 'municipality',)

admin.site.register(Navaid, NavaidAdmin)
