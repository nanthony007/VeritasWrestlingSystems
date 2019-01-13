from django.contrib import admin
from django.urls import path
from django.views.generic import ListView, DetailView
from vws_main.models import Wrestler, Timeseries
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('table/', ListView.as_view(queryset=Wrestler.objects.all().order_by('rating')[:10],
            template_name="vws_main/table.html"), name='wrestlers_table'),
    path('timeseries/', ListView.as_view(queryset=Timeseries.objects.all().order_by('-matchID', 'event_num')[:25],
            template_name="vws_main/timeseries.html"), name='timeseries_table')
]
