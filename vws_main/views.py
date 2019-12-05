from django.shortcuts import render
from django.db.models import Q, Avg, Sum, Count, Case, When, CharField, Value, FloatField, Func
from vws_main.models import FS_Event, FS_Wrestler, FS_Team, FS_Match
from django.views.generic import DetailView, ListView
from vws_main.forms import Wrestler1ModelForm
import pandas as pd
import os
from collections import Counter
from .Ecounter import effective_counter_rate
from .s3presign import create_presigned_url
from users.forms import LoginForm

def safe_div(x, y):
    """
    Accepts two numeric parameters.
    Safely divide first by second, even if second value is zero.
    """
    if y == 0:
        return x / (y + 1)
    else:
        return x / y


class Round(Func):
    function = 'ROUND'
    arity = 2


class FS_MatchDetailView(DetailView):
    queryset = FS_Match.objects.all().filter()
    template_name = "vws_main/fs-match-detail.html"


# class FS_MatchTableView(ListView):
#     queryset = FS_Match.objects.exclude(matchID__endswith='*').values('matchID', 'date', 'focus', 'opponent', 'focus_score', 'opp_score', 'result').order_by('-date', 'matchID')
#     template_name = "vws_main/fs_matchdata_table.html"


class FS_WrestlerDetailView(DetailView):
    template_name = "vws_main/fs-wrestler-detail.html"
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
            When(focus_wrestler2__result='LossF', then=Value(0.25)), output_field=FloatField())),
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
        total_vs=Sum('focus_wrestler2__vs'),

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

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        cwd = os.getcwd()
        matches = pd.read_csv(cwd + '/collection/stats/matchdata.csv', engine='python')
        wrestler = self.object.name
        matches = matches[matches.Focus == wrestler]
        data['matches'] = matches[matches.Duration != 0]
        rtc = Counter(matches['Result'])
        data['resulttypes'] = ['LossF', 'LossTF', 'LossD', 'WinD', 'WinTF', 'WinF']
        data['resulttypecounts'] = [rtc[i] for i in ['LossF', 'LossTF', 'LossD', 'WinD', 'WinTF', 'WinF']]
        vs = matches.VS
        data['vsindex'] = matches.MatchID.tolist()
        data['vsvalues'] = vs.tolist()
        data['worldvs'] = [17.66] * len(vs.index.tolist())
        # calculations
        HI = matches.HIa.sum()
        HO = matches.HOa.sum()
        D = matches.Da.sum()
        LS = matches.LSa.sum()
        GB = matches.GBa.sum()
        T = matches.Ta.sum()
        totalTDA = matches.HIa.sum() + matches.HOa.sum() + matches.Da.sum() + matches.LSa.sum() + matches.GBa.sum() + matches.Ta.sum()
        oHI = matches.oHIa.sum()
        oHO = matches.oHOa.sum()
        oD = matches.oDa.sum()
        oLS = matches.oLSa.sum()
        oGB = matches.oGBa.sum()
        oT = matches.oTa.sum()
        ototalTDA = matches.oHIa.sum() + matches.oHOa.sum() + matches.oDa.sum() + matches.oLSa.sum() + matches.oGBa.sum() + matches.oTa.sum()

        data['shot_labels'] = ['Head Inside', 'Head Outside', 'Double', 'LowShot', 'Counter', 'Throw']
        rates = [safe_div(matches.HIc2.sum() + matches.HIc4.sum(), matches.HIa.sum()) * 100,
                 safe_div(matches.HOc2.sum() + matches.HOc4.sum(), matches.HOa.sum()) * 100,
                 safe_div(matches.Dc2.sum() + matches.Dc4.sum(), matches.Da.sum()) * 100,
                 safe_div(matches.LSc2.sum() + matches.LSc4.sum(), matches.LSa.sum()) * 100,
                 safe_div(matches.GBc2.sum(), matches.GBa.sum()) * 100,
                 safe_div(matches.Tc2.sum() + matches.Tc4.sum(), matches.Ta.sum()) * 100]
        orates = [safe_div(matches.oHIc2.sum() + matches.oHIc4.sum(), matches.oHIa.sum()) * 100,
                  safe_div(matches.oHOc2.sum() + matches.oHOc4.sum(), matches.oHOa.sum()) * 100,
                  safe_div(matches.oDc2.sum() + matches.oDc4.sum(), matches.oDa.sum()) * 100,
                  safe_div(matches.oLSc2.sum() + matches.oLSc4.sum(), matches.oLSa.sum()) * 100,
                  safe_div(matches.oGBc2.sum(), matches.oGBa.sum()) * 100,
                  safe_div(matches.oTc2.sum() + matches.oTc4.sum(), matches.oTa.sum()) * 100]
        prefs = [(HI / totalTDA) * 100, (HO / totalTDA) * 100, (D / totalTDA) * 100, (LS / totalTDA) * 100,
                 (GB / totalTDA) * 100, (T / totalTDA) * 100]
        oprefs = [(oHI / ototalTDA) * 100, (oHO / ototalTDA) * 100, (oD / ototalTDA) * 100, (oLS / ototalTDA) * 100,
                 (oGB / ototalTDA) * 100, (oT / ototalTDA) * 100]
        data['rates'] = [round(i, 2) for i in rates]
        data['orates'] = [round(i, 2) for i in orates]
        data['prefs'] = [round(i, 2) for i in prefs]
        data['oprefs'] = [round(i, 2) for i in oprefs]

        # correlations
        matches_inter = matches.select_dtypes(exclude=['object'])
        matches_inter = matches_inter.drop(columns=['MoV', 'FocusPoints', 'OppPoints', 'BinaryResult', 'VS', 'oVS'])
        corrs = matches_inter.corr()['NumResult'][:-1].dropna()
        corrs = corrs[corrs > -1]
        corrs = corrs[corrs < 1]
        bad = corrs.sort_values(ascending=True)[:5]
        good = corrs.sort_values(ascending=False)[:5]
        data['badtitles'] = bad.index.tolist()
        data['badvalues'] = [round(i, 2) for i in bad]
        data['goodtitles'] = good.index.tolist()
        data['goodvalues'] = [round(i, 2) for i in good]
        ECR = effective_counter_rate(wrestler)
        data['focus_ecr'] = round(ECR[0], 2)
        data['opp_ecr'] = round(ECR[1], 2)
        return data


# class FS_TeamDetailView(DetailView):
#     queryset = FS_Team.objects.all().order_by('-team_name.all.rating')
#     template_name = 'vws_main/fs_team_detail.html'


# class FS_EventsListView(ListView):
#     template_name = 'vws_main/fs_events_table.html'

#     def get_queryset(self):
#         return FS_Event.objects.values('name', 'date').distinct().order_by('-date')


# class FS_EventsDetailView(DetailView):
#     template_name = 'vws_main/fs_events_detail.html'

#     def get_queryset(self):
#         return FS_Event.objects.filter()


class FS_RatingsFilterView(ListView):
    model = FS_Wrestler
    template_name = 'vws_main/fs-ratings.html'

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


def home(request):
    return render(request, 'vws_main/home.html')

def about(request):
    return render(request, "vws_main/about.html")

def resources(request):
    recording_manual = create_presigned_url('vws-django-profilepics', 'resources/Recording_Manual.docx')
    abbreviations = create_presigned_url('vws-django-profilepics', 'resources/VWSabbreviations.xlsx')
    context = {
        'recordingmanual': recording_manual,
        'abbreviations': abbreviations,
    }
    return render(request, "vws_main/resources.html", context=context)

def reportlist(request):
    return render(request, "vws_main/reports/feed.html")

def worldchampionships2019(request):
    return render(request, "vws_main/reports/worlds2019.html")

def sample(request):
    return render(request, "vws_main/reports/sample.html")
