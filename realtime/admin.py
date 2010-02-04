from django.contrib import admin
from models import Block, Duty

class BlockInline(admin.TabularInline):
    model = Block
    extra = 3

class DutyAdmin(admin.ModelAdmin):
    list_display = ('user', 'start', 'end', 'duty_length')
    inlines = (BlockInline, )

class BlockAdmin(admin.ModelAdmin):
    list_display = ('duty',
                    'block_start',
                    'airborne_start',
                    'airborne_end',
                    'block_end',
                    'block_time',
                    'airborne_time',
                    'is_valid',)         
                    
admin.site.register(Duty, DutyAdmin)    
admin.site.register(Block, BlockAdmin)
