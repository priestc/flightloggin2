from django.contrib.gis import admin
from models import Airport, Custom, Navaid, WorldBorders, USStates

class AirportAdmin(admin.OSMGeoAdmin):
    list_display = ('identifier', 'name', 'country', 'region', 'municipality',)
    search_fields = ('identifier', 'name', 'municipality',)

class CustomAdmin(admin.OSMGeoAdmin):
    list_display = ('identifier', 'name', 'country', 'region', 'municipality', 'user')
    search_fields = ('identifier', 'name', 'municipality',)
    
class NavaidAdmin(admin.OSMGeoAdmin):
    list_display = ('identifier', 'name', 'type',)
    search_fields = ('identifier', 'name',)

class WorldBordersAdmin(admin.OSMGeoAdmin):
    search_fields = ('name',)

class USStatesAdmin(admin.OSMGeoAdmin):
    search_fields = ('name',)

admin.site.register(Navaid, NavaidAdmin)
admin.site.register(Custom, CustomAdmin)
admin.site.register(Airport, AirportAdmin)
admin.site.register(WorldBorders, WorldBordersAdmin)
admin.site.register(USStates, USStatesAdmin)

