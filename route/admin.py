from django.contrib import admin
from models import *

class RouteBaseInline(admin.TabularInline):
    model = RouteBase
    extra = 3
    raw_id_fields = ('location', )

class RouteAdmin(admin.ModelAdmin):
    inlines = (RouteBaseInline,)
    search_fields = ('simple_rendered',)
    list_display = ('simple_rendered', 'max_width_all', 'total_line_all',
                    'p2p')

class RouteBaseAdmin(admin.ModelAdmin):
    search_fields = ('id',)
    list_display = ('location', 'unknown', 'land')
    raw_id_fields = ('location', )

####################################################

admin.site.register(Route, RouteAdmin)
admin.site.register(RouteBase, RouteBaseAdmin)
