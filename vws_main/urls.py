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
    path('matchdata/<pk>/', views.MatchDetailView.as_view(), name='match_detail_view'),
    path('wrestlers/<slug>/', views.WrestlerDetailView.as_view(), name='wrestler_detail_view'),
    path('teams/', views.TeamListView.as_view(), name='team_list'),
    path('teams/<slug>/', views.TeamDetailView.as_view(), name='team_roster'),
]
