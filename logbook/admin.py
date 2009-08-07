from django.contrib import admin
from models import *

admin.site.register(Columns)

admin.site.register(Flight)
admin.site.register(NonFlight)

admin.site.register(Route)
admin.site.register(RouteBase)
