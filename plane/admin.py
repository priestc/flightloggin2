from django.contrib import admin
from models import *

class PlaneAdmin(admin.ModelAdmin):
    list_display = ('tailnumber', 'user', 'manufacturer', 'type',
                    'model', 'fuel_burn', 'cat_class', 'tags')
    search_fields = ('tailnumber', 'type', 'tags', 'model')
    list_filter = ('cat_class', 'hidden', 'retired')
    
admin.site.register(Plane, PlaneAdmin)
