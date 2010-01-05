from django.contrib import admin
from models import *

class BlockInline(admin.TabularInline):
    model = DutyFlight
    extra = 3


class DutyAdmin(admin.ModelAdmin):
    list_display = ('user', 'start', 'end', 'duty_length')
    inlines = (BlockInline, )


class DutyFlightAdmin(admin.ModelAdmin):
    list_display = ('duty',
                    'block_start',
                    'airborne_start',
                    'airborne_end',
                    'block_end',
                    'block_time',
                    'airborne_time',
                    'is_valid',)
                    
                    
                    
                    
admin.site.register(Duty, DutyAdmin)    
admin.site.register(DutyFlight, DutyFlightAdmin)
