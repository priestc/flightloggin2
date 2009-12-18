from django.contrib import admin
from models import *

class ProfileAdmin(admin.ModelAdmin):
    search_fields = ('user__username', 'user__email')
    list_display = ('user', 'date_registered', 'real_name', 'get_email',
                    'date_format', 'adminlink')
    
    list_filter = ('backup_freq', 'style')

admin.site.register(Profile, ProfileAdmin)
