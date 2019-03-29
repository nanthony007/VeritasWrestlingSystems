from django.shortcuts import render
from django.db.models import Q, F, Avg, Sum, Count, Case, When, CharField, Value, FloatField
from vws_main.models import Matchdata, Wrestler, Team, Event
from django.views.generic import DetailView, ListView
from django_filters.views import FilterView
from vws_main.filters import RatingsFilter, EventsFilter


def home(request):
    return render(request, 'vws_main/home.html')


class MatchDetailView(DetailView):
    queryset = Matchdata.objects.all().filter()
    template_name = "vws_main/match_detail.html"


class MatchTableView(ListView):
    queryset = Matchdata.objects.exclude(matchID__endswith='_').values('matchID', 'date', 'focus', 'opponent', 'focus_score', 'opp_score', 'result').order_by('-date', 'matchID')
    template_name = "vws_main/matchdata_table.html"


class WrestlerDetailView(DetailView):
    template_name = "vws_main/wrestler_detail.html"
    slug_field = 'slug'
    queryset = Wrestler.objects.filter().annotate(
        match_count=Count('focus_wrestler'),
        points_earned=Sum('focus_wrestler__focus_score'),
        points_allowed=Sum('focus_wrestler__opp_score'),
        npf=Avg('focus_wrestler__npf'),
        vp=Sum('focus_wrestler__vs'),
        apm=Avg('focus_wrestler__apm'),
        oapm=Avg('focus_wrestler__opp_apm'),
        #npf=Avg('focus_wrestler__')
        avg_result=Avg(Case(
            When(focus_wrestler__result='WinF', then=Value(1.75)),
            When(focus_wrestler__result='WinTF', then=Value(1.50)),
            When(focus_wrestler__result='WinMD', then=Value(1.25)),
            When(focus_wrestler__result='WinD', then=Value(1.10)),
            When(focus_wrestler__result='LossD', then=Value(0.90)),
            When(focus_wrestler__result='LossMD', then=Value(0.75)),
            When(focus_wrestler__result='LossTF', then=Value(0.50)),
            When(focus_wrestler__result='LossF', then=Value(0.25)),
                output_field=FloatField()))
    )


class TeamListView(ListView):
    queryset = Team.objects.all()
    template_name = 'vws_main/team_table.html'


class TeamDetailView(DetailView):
    queryset = Team.objects.all().order_by('-team_name.all.rating')
    template_name = 'vws_main/team_detail.html'


class EventsListView(ListView):
    queryset = Event.objects.all()
    template_name = 'vws_main/events_table.html'

    def get_queryset(self):
        return Event.objects.values('name', 'date', 'result').distinct().order_by('-date')


class EventsDetailView(DetailView):
    queryset = Event.objects.all().order_by('-date')
    template_name = 'vws_main/events_detail.html'


class RatingsFilterView(FilterView):
    filterset_class = RatingsFilter
    template_name = 'vws_main/ratings.html'

    def get_queryset(request):
        return Wrestler.objects.annotate(
            tier=Case(
                When(rating__gte=2500, then=Value('Grandmaster')),
                When(Q(rating__lt=2500) & Q(rating__gte=2300), then=Value('Master')),
                When(Q(rating__lt=2300) & Q(rating__gte=2000), then=Value('Expert')),
                When(Q(rating__lt=2000) & Q(rating__gte=1800), then=Value('Class A')),
                When(Q(rating__lt=1800) & Q(rating__gte=1600), then=Value('Class B')),
                When(Q(rating__lt=1600) & Q(rating__gte=1400), then=Value('Class C')),
                When(Q(rating__lt=1400) & Q(rating__gte=1200), then=Value('Class D')),
                When(Q(rating__lt=1200) & Q(rating__gte=1000), then=Value('Class E')),
                When(Q(rating__lt=1000) & Q(rating__gte=700), then=Value('Amateur')),
                When(rating__lt=700, then=Value('Novice')),
                output_field=CharField(),
            ),
            weight=Case(
                When(focus_wrestler__weight=125, then=Value(125)),
                When(focus_wrestler__weight=133, then=Value(133)),
                When(focus_wrestler__weight=141, then=Value(141)),
                When(focus_wrestler__weight=149, then=Value(149)),
                When(focus_wrestler__weight=157, then=Value(157)),
                When(focus_wrestler__weight=165, then=Value(165)),
                When(focus_wrestler__weight=174, then=Value(174)),
                When(focus_wrestler__weight=184, then=Value(184)),
                When(focus_wrestler__weight=197, then=Value(197)),
                When(focus_wrestler__weight=285, then=Value(285)),
                output_field=FloatField(),
            )).values('name', 'team', 'rating', 'tier', 'weight', 'slug').distinct().order_by('-rating')
