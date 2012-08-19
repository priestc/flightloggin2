from django.contrib import admin
from models import *

class BadgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'awarded_date', 'level')
    search_fields = ('user', 'title')
    list_filter = ('title', )

admin.site.register(AwardedBadge, BadgeAdmin)