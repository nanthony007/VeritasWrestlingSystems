from django.contrib import admin
from vws_main.models import Wrestler, Timeseries, Matchdata, Team, Event, FS_Match, FS_TS, FS_Wrestler, FS_Team, FS_Event

# Register your models here.
class WrestlerAdmin(admin.ModelAdmin):
    list_display = ('name', 'team_id', 'rating')

class TimeseriesAdmin(admin.ModelAdmin):
    list_display = ('matchID', 'event_num', 'event_lab', 'event_time', 'red', 'blue')

class MatchdataAdmin(admin.ModelAdmin):
    list_display = ('matchID', 'date', 'focus_score', 'opp_score', 'result')

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbreviation', 'slug')

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')

class FS_MatchAdmin(admin.ModelAdmin):
    list_display = ('matchID', 'focus','opponent',
        'focus_score', 'opp_score', 'result')

class FS_TSAdmin(admin.ModelAdmin):
    list_display = ('matchID', 'event_num', 'event_lab', 'event_time', 'red', 'blue')

class FS_TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbreviation', 'slug')

class FS_WrestlerAdmin(admin.ModelAdmin):
    list_display = ('name', 'team_id', 'rating')

class FS_EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')

admin.site.register(Wrestler, WrestlerAdmin)
admin.site.register(Matchdata, MatchdataAdmin)
admin.site.register(Timeseries, TimeseriesAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(FS_Match, FS_MatchAdmin)
admin.site.register(FS_TS, FS_TSAdmin)
admin.site.register(FS_Wrestler, FS_WrestlerAdmin)
admin.site.register(FS_Team, FS_TeamAdmin)
admin.site.register(FS_Event, FS_EventAdmin)
