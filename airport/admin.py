from django.contrib import admin
from models import *

class LocationAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'name', 'country', 'region', 'municipality',
                    'user')
    search_fields = ('identifier', 'name', 'municipality',)
    list_filter = ('loc_class','loc_type')
    raw_id_fields = ('user', )

class RegionAdmin(admin.ModelAdmin):
    search_fields = ('name','code')
    list_display = ('name', 'code', 'country_name')

class HistoricalIdentAdmin(admin.ModelAdmin):
    raw_id_fields = ('current_location', )
    search_fields = ('identifier', 'current_location__identifier')
    list_display = ('identifier', 'current_location', 'curr_name', 'start', 'end')

class CountryAdmin(admin.ModelAdmin):
    search_fields = ('name','code')
    list_display = ('name', 'code')


admin.site.register(Location, LocationAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(HistoricalIdent, HistoricalIdentAdmin)
