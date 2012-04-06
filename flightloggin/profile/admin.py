from django.contrib import admin
from models import *

class ProfileAdmin(admin.ModelAdmin):
    search_fields = ('user__username', 'user__email')
    list_display = ('user', 'date_registered', 'real_name',
                    'get_email', 'get_date_format', 'adminlink', 'flightcount')
    list_filter = ('backup_freq', 'style', 'logbook_share', 'social')
    list_per_page = 20
    readonly_fields = ('get_openid', )

admin.site.register(Profile, ProfileAdmin)
