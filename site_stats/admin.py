from django.contrib import admin
from models import *

class StatsAdmin(admin.ModelAdmin):
    list_display = ('dt', 'total_hours', 'total_logged', 'users')
    
admin.site.register(StatDB, StatsAdmin)
