from django.contrib import admin
from django.urls import path
from django.views.generic import ListView, DetailView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('wrestlers/', views.WrestlerTableView.as_view(), name='wrestlers_table'),
    path('matchdata/', views.MatchTableView.as_view(), name='matchdata_table'),
    path('matchdata/<pk>/', views.MatchDetailView.as_view(), name='match_detail_view'),
    path('wrestlers/<slug>/', views.WrestlerDetailView.as_view(), name='wrestler_detail_view'),
    path('teams/', views.TeamListView.as_view(), name='team_list'),
    path('teams/<slug>/', views.TeamDetailView.as_view(), name='team_roster'),
    path('events/', views.EventsListView.as_view(), name='events_list'),
    path('events/<slug>/', views.EventsDetailView.as_view(), name='events_detail_view'),
    path('ratings/', views.RatingView.as_view(), name='rating_view'),
    path('weight_classes/', views.weightclasses, name='weight_classes'),
]
