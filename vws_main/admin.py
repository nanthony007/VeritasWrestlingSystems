from django.contrib import admin
from vws_main.models import FS_Match, FS_TS, FS_Wrestler, FS_Team, FS_Event


# Register your models here.
class FS_MatchAdmin(admin.ModelAdmin):
    list_display = ('matchID', 'focus','opponent',
        'focus_score', 'opp_score', 'result')


class FS_TSAdmin(admin.ModelAdmin):
    list_display = ('matchID', 'event_num', 'event_lab', 'event_time', 'red', 'blue')


class FS_TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbreviation', 'slug')


class FS_WrestlerAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating')


class FS_EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')



admin.site.register(FS_Match, FS_MatchAdmin)
admin.site.register(FS_TS, FS_TSAdmin)
admin.site.register(FS_Wrestler, FS_WrestlerAdmin)
admin.site.register(FS_Team, FS_TeamAdmin)
admin.site.register(FS_Event, FS_EventAdmin)
