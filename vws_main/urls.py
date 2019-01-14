from django.contrib import admin
from django.urls import path
from django.views.generic import ListView, DetailView
from vws_main.models import Wrestler, Timeseries, Matchdata
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('wrestlers/', views.WrestlerTableView.as_view(), name='wrestlers_table'),
    path('matchdata/', views.MatchTableView.as_view(), name='matchdata_table'),
    path('matchdata/<pk>/', views.MatchDetailView.as_view(), name='detail_view')
]
