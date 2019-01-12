from django.contrib import admin
from vws_main.models import Wrestler

# Register your models here.
class WrestlerAdmin(admin.ModelAdmin):
    list_display = ('athlete', 'team', 'eligibility', 'rating')

admin.site.register(Wrestler, WrestlerAdmin)
