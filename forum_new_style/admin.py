from django.contrib import admin
from models import *

class ForumAdmin(admin.ModelAdmin):
    list_display = ('name', 'force_anon', 'order', 'divider')
    search_fields = ('name', )

admin.site.register(Forum, ForumAdmin)
admin.site.register(Thread)
admin.site.register(Post)
