from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('matchdata/', views.MatchTableView.as_view(), name='matchdata_table'),
    path('matchdata/<pk>/', views.MatchDetailView.as_view(), name='match_detail_view'),
    path('wrestlers/<slug>/', views.WrestlerDetailView.as_view(), name='wrestler_detail_view'),
    path('teams/', views.TeamListView.as_view(), name='team_list'),
    path('teams/<slug>/', views.TeamDetailView.as_view(), name='team_roster'),
    path('events/', views.EventsListView.as_view(), name='events_list'),
    path('events/<slug>/', views.EventsDetailView.as_view(), name='events_detail_view'),
    path('ratings/', views.RatingsFilterView.as_view(), name='rating_view'),
]
