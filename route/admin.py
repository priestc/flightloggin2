from django.contrib import admin
from models import *

class RouteBaseInline(admin.TabularInline):
    model = RouteBase
    extra = 3
    raw_id_fields = ('location')

class RouteAdmin(admin.ModelAdmin):
    inlines = (RouteBaseInline,)
    search_fields = ('simple_rendered',)


####################################################

admin.site.register(Route, RouteAdmin)
admin.site.register(RouteBase)
