from django.contrib import admin
from vws_main.models import Wrestler, Timeseries, Matchdata, Team

# Register your models here.
class WrestlerAdmin(admin.ModelAdmin):
    list_display = ('name', 'eligibility', 'rating', 'slug')

class TimeseriesAdmin(admin.ModelAdmin):
    list_display = ('matchID', 'event_num', 'event_lab', 'event_time', 'red', 'blue')

class MatchdataAdmin(admin.ModelAdmin):
    list_display = ('matchID', 'date', 'blue_score', 'red_score', 'result')

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbreviation', 'slug')

admin.site.register(Wrestler, WrestlerAdmin)
admin.site.register(Matchdata, MatchdataAdmin)
admin.site.register(Timeseries, TimeseriesAdmin)
admin.site.register(Team, TeamAdmin)
