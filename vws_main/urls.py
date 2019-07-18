from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    #path('fs_matchdata/', views.FS_MatchTableView.as_view(), name='fs_matchdata_table'),
    path('fs_matchdata/<pk>/', views.FS_MatchDetailView.as_view(), name='fs_match_detail_view'),
    path('fs_wrestlers/<slug>/', views.FS_WrestlerDetailView.as_view(), name='fs_wrestler_detail_view'),
    #path('fs_teams/<slug>/', views.FS_TeamDetailView.as_view(), name='fs_team_roster'),
    #path('fs_events/', views.FS_EventsListView.as_view(), name='fs_events_list'),
    #path('fs_events/<slug>/', views.FS_EventsDetailView.as_view(), name='fs_events_detail_view'),
    path('fs_ratings/', views.FS_RatingsFilterView.as_view(), name='fs_rating_view'),
    path('compare/', views.compare_view, name='compare')
]
