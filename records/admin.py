from django.contrib import admin
from models import *

class NonFlightAdmin(admin.ModelAdmin):
    search_fields = ('user',)
    list_display = ('user', 'date', 'non_flying', 'remarks')
    list_filter = ('non_flying', )

class RecordsAdmin(admin.ModelAdmin):
    search_fields = ('user',)
    list_display = ('user', 'has_something', 'adminlink')


admin.site.register(Records, RecordsAdmin)
admin.site.register(NonFlight, NonFlightAdmin)
