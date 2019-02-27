from django.contrib import admin
from vws_main.models import Wrestler, Timeseries, Matchdata, Team, Event

# Register your models here.
class WrestlerAdmin(admin.ModelAdmin):
    list_display = ('name', 'team_id', 'eligibility', 'rating')

class TimeseriesAdmin(admin.ModelAdmin):
    list_display = ('matchID', 'event_num', 'event_lab', 'event_time', 'red', 'blue')

class MatchdataAdmin(admin.ModelAdmin):
    list_display = ('matchID', 'date', 'focus_score', 'opp_score', 'result')

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbreviation', 'slug')

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')

admin.site.register(Wrestler, WrestlerAdmin)
admin.site.register(Matchdata, MatchdataAdmin)
admin.site.register(Timeseries, TimeseriesAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Event, EventAdmin)
