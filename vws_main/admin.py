from django.contrib import admin
from vws_main.models import Wrestler, Timeseries, Matchdata

# Register your models here.
class WrestlerAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'eligibility', 'rating')


class TimeseriesAdmin(admin.ModelAdmin):
    list_display = ('matchID', 'event_num', 'event_lab', 'event_time', 'red', 'blue')

class MatchdataAdmin(admin.ModelAdmin):
    list_display = ('matchID', 'date', 'blue', 'red', 'blue_score', 'red_score', 'result')


admin.site.register(Wrestler, WrestlerAdmin)
admin.site.register(Matchdata, MatchdataAdmin)
