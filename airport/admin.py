from django.contrib.gis import admin
from models import *

class LocationAdmin(admin.OSMGeoAdmin):
    list_display = ('identifier', 'name', 'country', 'region', 'municipality',
                    'user')
    search_fields = ('identifier', 'name', 'municipality',)
    list_filter = ('loc_class','loc_type')
    raw_id_fields = ('user', )

class WorldBordersAdmin(admin.OSMGeoAdmin):
    search_fields = ('name','iso2')
    list_display = ('name', 'iso2',)

class USStatesAdmin(admin.OSMGeoAdmin):
    search_fields = ('name','state',)
    list_display = ('name', 'state',)
    
class RegionAdmin(admin.OSMGeoAdmin):
    search_fields = ('name','code')
    list_display = ('name', 'code', 'country_name')
    
class HistoricalIdentAdmin(admin.OSMGeoAdmin):
    raw_id_fields = ('current_location', )

admin.site.register(Location, LocationAdmin)
admin.site.register(WorldBorders, WorldBordersAdmin)
admin.site.register(USStates, USStatesAdmin)
admin.site.register(Country)
admin.site.register(Region, RegionAdmin)
admin.site.register(HistoricalIdent, HistoricalIdentAdmin)
