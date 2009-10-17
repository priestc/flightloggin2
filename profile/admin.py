from django.contrib import admin
from models import *

class ProfileAdmin(admin.ModelAdmin):
    search_fields = ('user',)
    list_display = ('user', 'share', 'real_name', 'date_format',
                    Profile.adminlink)

admin.site.register(Profile, ProfileAdmin)
