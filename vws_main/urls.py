from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('resources/', views.resources, name='resources'),
    path('analysis/feed/', views.reportlist, name='report-list'),
    #path('analysis/<slug>/', views.ReportDetailView.as_view(), name='report_detail'),
    #path('fs_matchdata/', views.FS_MatchTableView.as_view(), name='fs_matchdata_table'),
    path('matchdata/<pk>/', views.FS_MatchDetailView.as_view(),
         name='fs_match_detail_view'),
    path('wrestlers/<slug>/', views.FS_WrestlerDetailView.as_view(),
         name='fs_wrestler_detail_view'),
    #path('fs_teams/<slug>/', views.FS_TeamDetailView.as_view(), name='fs_team_roster'),
    #path('fs_events/', views.FS_EventsListView.as_view(), name='fs_events_list'),
    #path('fs_events/<slug>/', views.FS_EventsDetailView.as_view(), name='fs_events_detail_view'),
    path('ratings/', views.FS_RatingsFilterView.as_view(), name='fs_rating_view'),
]
