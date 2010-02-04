from django.contrib import admin
from models import *

class ProfileAdmin(admin.ModelAdmin):
    search_fields = ('user__username', 'user__email')
    list_display = ('user', 'date_registered', 'real_name', 'get_email',
                    'date_format', 'adminlink', 'flightcount')
    
    list_filter = ('backup_freq', 'style', 'logbook_share', 'social')

admin.site.register(Profile, ProfileAdmin)
