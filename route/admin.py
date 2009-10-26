from django.contrib import admin
from models import *


def hard_render(modeladmin, request, queryset):
    for r in queryset:
        r.hard_render()
        
hard_render.short_description = "Hard Render"

####################################################

class RouteBaseInline(admin.TabularInline):
    model = RouteBase
    extra = 3
    raw_id_fields = ('location', )

class RouteAdmin(admin.ModelAdmin):
    inlines = (RouteBaseInline,)
    search_fields = ('simple_rendered',)
    actions = (hard_render, )
    list_display = ('simple_rendered', 'max_width_all', 'total_line_all',
                    'p2p', Route.owner)

class RouteBaseAdmin(admin.ModelAdmin):
    search_fields = ('id',)
    list_display = ('location', 'unknown', 'land', RouteBase.admin_loc_class,
                     RouteBase.owner)
    raw_id_fields = ('location', )
    
####################################################

admin.site.register(Route, RouteAdmin)
admin.site.register(RouteBase, RouteBaseAdmin)
