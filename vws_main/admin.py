from django.contrib import admin
from vws_main.models import Wrestler, Timeseries

# Register your models here.
class WrestlerAdmin(admin.ModelAdmin):
    list_display = ('athlete', 'team', 'eligibility', 'rating')


class TimeseriesAdmin(admin.ModelAdmin):
    list_display = ('matchID', 'event_num', 'event_lab', 'event_time', 'red', 'blue')

admin.site.register(Wrestler, WrestlerAdmin)
admin.site.register(Timeseries, TimeseriesAdmin)
