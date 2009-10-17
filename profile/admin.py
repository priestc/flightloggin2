from django.contrib import admin
from models import *

class ProfileAdmin(admin.ModelAdmin):
    search_fields = ('user',)
    list_display = ('user', 'date_registered', 'share', 'real_name',
                    'date_format', 'adminlink')

admin.site.register(Profile, ProfileAdmin)
