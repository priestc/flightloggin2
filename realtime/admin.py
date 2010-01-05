from django.contrib import admin
from models import *

class DutyAdmin(admin.ModelAdmin):
    list_display = ('user', 'start', 'end', 'duty_length')
    
admin.site.register(Duty, DutyAdmin)

class DutyFlightAdmin(admin.ModelAdmin):
    list_display = ('duty', 'block_start',
                            'airborne_start',
                            'airborne_end',
                            'block_end',
                    'block_time',
                    'airborne_time',
                    'is_valid',)
    
admin.site.register(DutyFlight, DutyFlightAdmin)
