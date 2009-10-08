from django.contrib.gis import admin
from models import Airport, Custom, Navaid, WorldBorders

class AirportAdmin(admin.GeoModelAdmin):
    list_display = ('identifier', 'name', 'country', 'region', 'municipality',)
    search_fields = ('identifier', 'name', 'municipality',)

class CustomAdmin(admin.GeoModelAdmin):
    list_display = ('identifier', 'name', 'country', 'region', 'municipality', 'user')
    search_fields = ('identifier', 'name', 'municipality',)
    
class NavaidAdmin(admin.GeoModelAdmin):
    list_display = ('identifier', 'name', 'type',)
    search_fields = ('identifier', 'name',)

class WorldBordersAdmin(admin.GeoModelAdmin):
    search_fields = ('name',)

admin.site.register(Navaid, NavaidAdmin)
admin.site.register(Custom, CustomAdmin)
admin.site.register(Airport, AirportAdmin)
admin.site.register(WorldBorders, WorldBordersAdmin)
