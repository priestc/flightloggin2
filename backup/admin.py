from django.contrib import admin
from models import UsersToday

class UsersTodayAdmin(admin.ModelAdmin):
    list_display = ('date', 'users_count', 'usernames', 'email_usernames')
    raw_id_fields = ('logged_today', )
    list_per_page = 14

admin.site.register(UsersToday, UsersTodayAdmin)
