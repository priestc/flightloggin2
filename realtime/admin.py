from django.contrib import admin
from models import *

class DutyAdmin(admin.ModelAdmin):
    list_display = ('user', 'start', 'end')
    
admin.site.register(Duty, DutyAdmin)
