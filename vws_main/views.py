from django.shortcuts import render
from django.db.models import Q, Avg, Sum, Count, Case, When, CharField, Value, FloatField, Func
from vws_main.models import FS_Event, FS_Wrestler, FS_Team, FS_Match
from django.views.generic import DetailView, ListView
from django_filters.views import FilterView
from vws_main.filters import FS_RatingsFilter
import pandas as pd
import matplotlib.pyplot as plt
from django.urls import reverse
from django.http import HttpResponse
import seaborn as sns
import os
import io

class Round(Func):
    function = 'ROUND'
    arity = 2


def graph(request):
    cwd = os.getcwd()
    matches = pd.read_csv(cwd + '/collection/stats/matchdata.csv', engine='python')
    matches = matches[matches.focus_id == 'Zain Retherford']
    matches = matches[matches.duration != 0]
    # calculations
    HIC = matches.hia.sum()
    HOC = matches.hoa.sum()
    DC = matches.da.sum()
    LSC = matches.lsa.sum()
    GBC = matches.gba.sum()
    TC = matches.ta.sum()
    totalTDA = matches.hia.sum() + matches.hoa.sum() + matches.da.sum() + matches.lsa.sum() + matches.gba.sum() + matches.ta.sum()
    oHIC = matches.opp_hia.sum()
    oHOC = matches.opp_hoa.sum()
    oDC = matches.opp_da.sum()
    oLSC = matches.opp_lsa.sum()
    oGBC = matches.opp_gba.sum()
    oTC = matches.opp_ta.sum()
    ototalTDA = matches.opp_hia.sum() + matches.opp_hoa.sum() + matches.opp_da.sum() + matches.opp_lsa.sum() + matches.opp_gba.sum() + matches.opp_ta.sum()
    # sets up dataframes
    shot_labels = ['Head Inside', 'Head Outside', 'Double', 'LowShot', 'Counter', 'Throw',
                   'Head Inside', 'Head Outside', 'Double', 'LowShot', 'Counter', 'Throw']
    athlete = ['Focus', 'Focus', 'Focus', 'Focus', 'Focus', 'Focus',
               'Opponent', 'Opponent', 'Opponent', 'Opponent', 'Opponent', 'Opponent']
    rates = [matches.hi_rate.mean(), matches.ho_rate.mean(), matches.d_rate.mean(), matches.ls_rate.mean(),
             matches.gb_rate.mean(),
             matches.t_rate.mean(),
             matches.opp_hi_rate.mean(), matches.opp_ho_rate.mean(), matches.opp_d_rate.mean(),
             matches.opp_ls_rate.mean(),
             matches.gb_rate.mean(), matches.opp_t_rate.mean()]
    prefs = [(HIC / totalTDA) * 100, (HOC / totalTDA) * 100, (DC / totalTDA) * 100, (LSC / totalTDA) * 100,
             (GBC / totalTDA) * 100, (TC / totalTDA) * 100,
             (oHIC / ototalTDA) * 100, (oHOC / ototalTDA) * 100, (oDC / ototalTDA) * 100, (oLSC / ototalTDA) * 100,
             (oGBC / ototalTDA) * 100, (oTC / ototalTDA) * 100]
    rate_df = pd.DataFrame()
    rate_df['wrestler'] = athlete
    rate_df['shottype'] = shot_labels
    rate_df['rate'] = rates
    rate_df['pref'] = prefs
    # correlations
    matches_inter = matches.select_dtypes(exclude=['object'])
    matches_inter = matches_inter.drop(columns=['mov', 'focus_score', 'opp_score', 'num_result'])
    corrs = matches_inter.corr()['binary_result'][:-1].dropna()
    corrs = corrs[corrs > -1]
    corrs = corrs[corrs < 1]
    bad = corrs.sort_values(ascending=True)[:10]
    good = corrs.sort_values(ascending=False)[:10]

    # plot
    sns.set_style('white', {'axes.spines.right': False, 'axes.spines.top': False})
    fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize=(16, 9))
    plt.subplots_adjust(wspace=0.50, hspace=0.50)
    g1 = sns.countplot(y='result_type', hue='binary_result_text', data=matches,
                       order=['', 'Fall', 'Tech', 'Decision'],
                       palette=sns.diverging_palette(240, 10, n=2), ax=ax1)
    ax1.set_title('Results')
    ax1.set_xlabel("Count")
    ax1.set_ylabel("Result Type")
    ax1.legend(loc='upper center', ncol=2, frameon=False)
    g2 = sns.lineplot(data=matches, x=range(1, len(matches.index) + 1), y='vs', ax=ax2)
    ax2.axhline(matches.vs.mean(), label='World Average', color='gold')
    ax2.set_title("Veritas Score")
    ax2.set_xlabel("Matches")
    ax2.set_ylabel("VS")
    ax2.legend(loc='upper center', frameon=False)
    ax2.legend_.set_title("")
    g3 = sns.barplot(x='pref', y='shottype', hue='wrestler', data=rate_df,
                     palette=sns.diverging_palette(240, 10, n=2), ax=ax3)
    ax3.set_title('Preference')
    ax3.set_xlabel("Preference (% of total shots)")
    ax3.set_ylabel("Shot Type")
    ax3.legend(loc='center right', frameon=False)
    ax3.legend_.set_title("")
    g4 = sns.barplot(x='rate', y='shottype', hue='wrestler', data=rate_df,
                     palette=sns.diverging_palette(240, 10, n=2), ax=ax4)
    ax4.set_title('Effeciency')
    ax4.set_xlabel("Effeciency Rate (%)")
    ax4.legend(loc="center right", frameon=False)
    ax4.legend_.set_title("")
    g5 = sns.barplot(x=good.values, y=good.index, palette=sns.light_palette("darkblue", 10, reverse=True), ax=ax5)
    ax5.set_title('Good Actions (Top 10)')
    ax5.set_xlabel("Correlation to Winning")
    ax5.set_ylabel("Action")
    g6 = sns.barplot(x=bad.values, y=bad.index, palette=sns.light_palette("crimson", 10, reverse=True), ax=ax6)
    ax6.set_title('Bad Actions (Top 10)')
    ax6.set_xlabel("Correlation to Winning")
    ax6.set_ylabel("Action")
    plt.suptitle('Wrestler Report Metrics', size=16)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    response = HttpResponse(buf.getvalue(), content_type='image/png')
    return response


class FS_ReportsView(ListView):
    template_name = 'vws_main/reports_detail.html'
    slug_field = 'slug'

    def get_queryset(self):
        return FS_Match.objects.filter(focus__slug=self.kwargs['slug']).exclude(duration='00:00:00')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        first = self.kwargs['slug'].split('-')[0].capitalize()
        last = self.kwargs['slug'].split('-')[1].capitalize()
        data['name'] = first + ' ' + last
        return data


def home(request):
    return render(request, 'vws_main/home.html')


class FS_MatchDetailView(DetailView):
    queryset = FS_Match.objects.all().filter()
    template_name = "vws_main/fs_match_detail.html"


class FS_MatchTableView(ListView):
    queryset = FS_Match.objects.exclude(matchID__endswith='*').values('matchID', 'date', 'focus', 'opponent', 'focus_score', 'opp_score', 'result').order_by('-date', 'matchID')
    template_name = "vws_main/fs_matchdata_table.html"


class FS_WrestlerDetailView(DetailView):
    template_name = "vws_main/fs_wrestler_detail.html"
    slug_field = 'slug'
    queryset = FS_Wrestler.objects.filter().annotate(
        match_count=Count('focus_wrestler2'),
        avg_result=Avg(Case(
            When(focus_wrestler2__result='WinF', then=Value(1.75)),
            When(focus_wrestler2__result='WinTF', then=Value(1.50)),
            When(focus_wrestler2__result='WinMD', then=Value(1.25)),
            When(focus_wrestler2__result='WinD', then=Value(1.10)),
            When(focus_wrestler2__result='LossD', then=Value(0.90)),
            When(focus_wrestler2__result='LossMD', then=Value(0.75)),
            When(focus_wrestler2__result='LossTF', then=Value(0.50)),
            When(focus_wrestler2__result='LossF', then=Value(0.25)),
                output_field=FloatField())),
        # focus base stats
        hia=Sum('focus_wrestler2__hia'),
        hic2=Sum('focus_wrestler2__hic2'),
        hic4=Sum('focus_wrestler2__hic4'),
        hoa=Sum('focus_wrestler2__hoa'),
        hoc2=Sum('focus_wrestler2__hoc2'),
        hoc4=Sum('focus_wrestler2__hoc4'),
        da=Sum('focus_wrestler2__da'),
        dc2=Sum('focus_wrestler2__dc2'),
        dc4=Sum('focus_wrestler2__dc4'),
        lsa=Sum('focus_wrestler2__lsa'),
        lsc2=Sum('focus_wrestler2__lsc2'),
        lsc4=Sum('focus_wrestler2__lsc4'),
        gba=Sum('focus_wrestler2__gba'),
        gbc2=Sum('focus_wrestler2__gbc2'),
        ta=Sum('focus_wrestler2__ta'),
        tc2=Sum('focus_wrestler2__tc2'),
        tc4=Sum('focus_wrestler2__tc4'),
        exposure=Sum('focus_wrestler2__exposure'),
        gut=Sum('focus_wrestler2__gut'),
        leg_lace=Sum('focus_wrestler2__leg_lace'),
        turn=Sum('focus_wrestler2__turn'),

        # opp base stats
        opp_hia=Sum('focus_wrestler2__opp_hia'),
        opp_hic2=Sum('focus_wrestler2__opp_hic2'),
        opp_hic4=Sum('focus_wrestler2__opp_hic4'),
        opp_hoa=Sum('focus_wrestler2__opp_hoa'),
        opp_hoc2=Sum('focus_wrestler2__opp_hoc2'),
        opp_hoc4=Sum('focus_wrestler2__opp_hoc4'),
        opp_da=Sum('focus_wrestler2__opp_da'),
        opp_dc2=Sum('focus_wrestler2__opp_dc2'),
        opp_dc4=Sum('focus_wrestler2__opp_dc4'),
        opp_lsa=Sum('focus_wrestler2__opp_lsa'),
        opp_lsc2=Sum('focus_wrestler2__opp_lsc2'),
        opp_lsc4=Sum('focus_wrestler2__opp_lsc4'),
        opp_gba=Sum('focus_wrestler2__opp_gba'),
        opp_gbc2=Sum('focus_wrestler2__opp_gbc2'),
        opp_ta=Sum('focus_wrestler2__opp_ta'),
        opp_tc2=Sum('focus_wrestler2__opp_tc2'),
        opp_tc4=Sum('focus_wrestler2__opp_tc4'),
        opp_exposure=Sum('focus_wrestler2__opp_exposure'),
        opp_gut=Sum('focus_wrestler2__opp_gut'),
        opp_leg_lace=Sum('focus_wrestler2__opp_leg_lace'),
        opp_turn=Sum('focus_wrestler2__opp_turn'),

        # focus adv stats
        hi_rate=Avg('focus_wrestler2__hi_rate'),
        ho_rate=Avg('focus_wrestler2__ho_rate'),
        d_rate=Avg('focus_wrestler2__d_rate'),
        ls_rate=Avg('focus_wrestler2__ls_rate'),
        gb_rate=Avg('focus_wrestler2__gb_rate'),
        t_rate=Avg('focus_wrestler2__t_rate'),
        npf=Avg('focus_wrestler2__npf'),
        apm=Avg('focus_wrestler2__apm'),
        vs=Avg('focus_wrestler2__vs'),

        # opp adv stats
        opp_hi_rate=Avg('focus_wrestler2__opp_hi_rate'),
        opp_ho_rate=Avg('focus_wrestler2__opp_ho_rate'),
        opp_d_rate=Avg('focus_wrestler2__opp_d_rate'),
        opp_ls_rate=Avg('focus_wrestler2__opp_ls_rate'),
        opp_gb_rate=Avg('focus_wrestler2__opp_gb_rate'),
        opp_t_rate=Avg('focus_wrestler2__opp_t_rate'),
        opp_npf=Avg('focus_wrestler2__opp_npf'),
        opp_apm=Avg('focus_wrestler2__opp_apm'),
        opp_vs=Avg('focus_wrestler2__opp_vs'),

        # misc
        points_earned=Sum('focus_wrestler2__focus_score'),
        points_allowed=Sum('focus_wrestler2__opp_score'),
        # turn_rate=
        recovery=Sum('focus_wrestler2__recovery'),
        opp_recovery=Sum('focus_wrestler2__opp_recovery'),
        pushout=Sum('focus_wrestler2__pushout'),
        opp_pushout=Sum('focus_wrestler2__opp_pushout'),
        passive=Sum('focus_wrestler2__passive'),
        opp_passive=Sum('focus_wrestler2__opp_passive'),
        violation=Sum('focus_wrestler2__violation'),
        opp_violation=Sum('focus_wrestler2__opp_violation')
        )


class FS_TeamDetailView(DetailView):
    queryset = FS_Team.objects.all().order_by('-team_name.all.rating')
    template_name = 'vws_main/fs_team_detail.html'


class FS_EventsListView(ListView):
    template_name = 'vws_main/fs_events_table.html'

    def get_queryset(self):
        return FS_Event.objects.values('name', 'date').distinct().order_by('-date')


class FS_EventsDetailView(DetailView):
    template_name = 'vws_main/fs_events_detail.html'

    def get_queryset(self):
        return FS_Event.objects.filter()


class FS_RatingsFilterView(FilterView):
    model = FS_Wrestler
    filterset_class = FS_RatingsFilter
    template_name = 'vws_main/fs_ratings.html'
    paginate_by = 25

    def get_queryset(request):
        return FS_Wrestler.objects.annotate(
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
                When(focus_wrestler2__weight=57, then=Value(57)),
                When(focus_wrestler2__weight=61, then=Value(61)),
                When(focus_wrestler2__weight=65, then=Value(65)),
                When(focus_wrestler2__weight=70, then=Value(70)),
                When(focus_wrestler2__weight=74, then=Value(74)),
                When(focus_wrestler2__weight=79, then=Value(79)),
                When(focus_wrestler2__weight=86, then=Value(86)),
                When(focus_wrestler2__weight=92, then=Value(92)),
                When(focus_wrestler2__weight=97, then=Value(97)),
                When(focus_wrestler2__weight=125, then=Value(125)),
                output_field=FloatField(),
            ),
            match_count=Count('focus_wrestler2__matchID')
            ).filter(match_count__gt=0).distinct().order_by('-rating')
