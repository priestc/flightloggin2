from django.contrib import admin
from models import UsersToday

class UsersTodayAdmin(admin.ModelAdmin):
    list_display = ('date', 'users_count', 'usernames')
    raw_id_fields = ('logged_today', )

admin.site.register(UsersToday, UsersTodayAdmin)
