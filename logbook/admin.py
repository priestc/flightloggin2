from django.contrib import admin
from models import *

class FlightAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'plane', 'route', 'remarks', )
    search_fields = ('user', 'remarks')
    raw_id_fields = ('plane', 'route')
    #filter_horizontal = ('user', )

admin.site.register(Flight, FlightAdmin)
admin.site.register(Columns)
