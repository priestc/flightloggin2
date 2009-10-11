from django.contrib.gis import admin
from models import *

class LocationAdmin(admin.OSMGeoAdmin):
    list_display = ('identifier', 'name', 'country', 'region', 'municipality',)
    search_fields = ('identifier', 'name', 'municipality',)

class WorldBordersAdmin(admin.OSMGeoAdmin):
    search_fields = ('name','iso2')
    list_display = ('name', 'iso2',)

class USStatesAdmin(admin.OSMGeoAdmin):
    search_fields = ('name','state',)
    list_display = ('name', 'state',)

admin.site.register(Location, LocationAdmin)
admin.site.register(WorldBorders, WorldBordersAdmin)
admin.site.register(USStates, USStatesAdmin)
admin.site.register(Country)
admin.site.register(Region)
