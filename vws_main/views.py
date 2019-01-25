from django.shortcuts import render
from vws_main.models import Matchdata, Wrestler, Team, Event
from django.views.generic import DetailView, ListView


def home(request):
    return render(request, 'vws_main/home.html')

def contact(request):
    return render(request, 'vws_main/contact.html')

class MatchDetailView(DetailView):
    queryset = Matchdata.objects.all().filter()
    template_name = "vws_main/match_detail.html"

class MatchTableView(ListView):
    queryset = Matchdata.objects.exclude(matchID__endswith='_').values('matchID', 'date', 'focus', 'opponent', 'focus_score', 'opp_score', 'result').order_by('-date')
    template_name = "vws_main/matchdata_table.html"

class WrestlerTableView(ListView):
    queryset = Wrestler.objects.values('name', 'team', 'rating').order_by('-rating')
    template_name = "vws_main/wrestler_table.html"

class WrestlerDetailView(DetailView):
    queryset = Wrestler.objects.filter()
    template_name = "vws_main/wrestler_detail.html"
    slug_field = 'slug'

class TeamListView(ListView):
    queryset = Team.objects.all()
    template_name = 'vws_main/team_table.html'

class TeamDetailView(DetailView):
    queryset = Team.objects.order_by('-team_name.name')
    template_name = 'vws_main/team_detail.html'

class EventsListView(ListView):
    queryset = Event.objects.values('name', 'slug')
    template_name = 'vws_main/events_table.html'

class EventsDetailView(DetailView):
    queryset = Event.objects.all()
    template_name = 'vws_main/events_detail.html'
