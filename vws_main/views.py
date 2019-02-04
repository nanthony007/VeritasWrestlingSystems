from django.shortcuts import render
from django.db.models import Q, Case, When, CharField, Value
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
    queryset = Matchdata.objects.exclude(matchID__endswith='_').values('matchID', 'date', 'focus', 'opponent', 'focus_score', 'opp_score', 'result').order_by('-date', 'matchID')
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
    queryset = Team.objects.all()
    template_name = 'vws_main/team_detail.html'

class EventsListView(ListView):
    queryset = Event.objects.values('name', 'date').order_by('-date')
    template_name = 'vws_main/events_table.html'

class EventsDetailView(DetailView):
    queryset = Event.objects.all().order_by('-date')
    template_name = 'vws_main/events_detail.html'

class RatingView(ListView):
    template_name = 'vws_main/ratings.html'
    queryset = Wrestler.objects.annotate(
        level=Case(
            When(rating__gte=2500, then=Value('Grandmaster')),
            When(Q(rating__lt=2500) & Q(rating__gte=2300), then=Value('Master')),
            When(Q(rating__lt=2300) & Q(rating__gte=2000), then=Value('Expert')),
            When(Q(rating__lt=2000) & Q(rating__gte=1800), then=Value('Class A')),
            When(Q(rating__lt=1800) & Q(rating__gte=1600), then=Value('Class B')),
            When(Q(rating__lt=1600) & Q(rating__gte=1400), then=Value('Class C')),
            When(Q(rating__lt=1400) & Q(rating__gte=1200), then=Value('Class D')),
            When(Q(rating__lt=1200) & Q(rating__gte=1000), then=Value('Class E')),
            When(Q(rating__lt=1000) & Q(rating__gte=800), then=Value('Amateur')),
            When(rating__lte=700, then=Value('Novice')),
            output_field=CharField(),
        )
    ).values('name', 'rating', 'level').order_by('-rating')
