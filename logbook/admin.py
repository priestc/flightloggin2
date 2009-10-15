from django.contrib import admin
from models import *

class FlightAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'plane', 'route', 'remarks', )
    search_fields = ('user', 'remarks')
    raw_id_fields = ('plane', 'route')
    #filter_horizontal = ('user', )
    
class ColumnAdmin(admin.ModelAdmin):
    list_display = ('user', 'f_route', 'line_dist','max_width','speed',
                    'student','fo','captain','instructor')

admin.site.register(Flight, FlightAdmin)
admin.site.register(Columns, ColumnAdmin)
