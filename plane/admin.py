from django.contrib import admin
from models import *

class PlaneAdmin(admin.ModelAdmin):
    list_display = ('tailnumber', 'user', 'manufacturer', 'type', 'model', 'cat_class', 'tags')
    search_fields = ('tailnumber', 'type', 'tags', 'model')
    list_filter = ('cat_class', 'hidden', 'retired')
    #filter_horizontal = ('tags', )
    
admin.site.register(Plane, PlaneAdmin)
