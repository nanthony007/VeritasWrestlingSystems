import csv, time
from vws_main.models import Wrestler, Timeseries, Matchdata, Team
from django.template.defaultfilters import slugify


""" Use this file to upload csv files to django database"""


# team table, delete and rewrite
#print('Stage 0')
#Team.objects.all().delete()

#with open('C:\\Users\HotRod\wrestling_app\collector_files\\rosters_teams.csv') as f:
#    reader = csv.DictReader(f)
#    for row in reader:
#        p = Team(
#            name=row['TeamName'],
#            abbreviation=row['Abbreviation']
#            )
#        p.save()

#for obj in Team.objects.all():
#    obj.slug = slugify(obj.name)
#    obj.save()

#print(time.perf_counter())


# wrestlers table, delete and rewrite
print('Stage 1')
Wrestler.objects.all().delete()

with open('C:\\Users\HotRod\wrestling_app\collector_files\wrestlers.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        p = Wrestler(
            name=row['WrestlerName'],
            team=Team.objects.get(name=row['Team']),
            eligibility=row['Eligibility'],
            rating=row['EloRating'],
            competitions=row['Matches'],
            )
        p.save()

for obj in Wrestler.objects.all():
    obj.slug = slugify(obj.name)
    obj.save()

print(time.perf_counter())


# matchdata table, delete and rewrite
print('Stage 2')
Matchdata.objects.all().delete()

with open('C:\\Users\HotRod\wrestling_app\collector_files\matchdata.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        p = Matchdata(
            matchID=row['MatchID'],
            date=row['Date'],
            focus=Wrestler.objects.get(name=row['Focus']),
            focus_team=Team.objects.get(name=row['FocusTeam']),
            opponent=Wrestler.objects.get(name=row['Opponent']),
            opp_team=Team.objects.get(name=row['OppTeam']),
            focus_score=row['FocusPoints'],
            opp_score=row['OppPoints'],
            result=row['Result'],
            weight=row['Weight'],
            mov=row['MoV'],
            duration=row['Time'],
            hia=row['HIa'],
            hic=row['HIc'],
            hoa=row['HOa'],
            hoc=row['HOc'],
            da=row['Da'],
            dc=row['Dc'],
            lsa=row['LSa'],
            lsc=row['LSc'],
            gba=row['GBa'],
            gbc=row['GBc'],
            ta=row['Ta'],
            tc=row['Tc'],
            su=row['SU'],
            e=row['E'],
            r=row['R'],
            cut=row['Cut'],
            bd=row['BD'],
            mr=row['MR'],
            nf2=row['NF2'],
            nf4=row['NF4'],
            caution=row['Caution'],
            tv=row['TV'],
            rt=row['RT'],
            opp_hia=row['oHIa'],
            opp_hic=row['oHIc'],
            opp_hoa=row['oHOa'],
            opp_hoc=row['oHOc'],
            opp_da=row['oDa'],
            opp_dc=row['oDc'],
            opp_lsa=row['oLSa'],
            opp_lsc=row['oLSc'],
            opp_gba=row['oGBa'],
            opp_gbc=row['oGBc'],
            opp_ta=row['oTa'],
            opp_tc=row['oTc'],
            opp_su=row['oSU'],
            opp_e=row['oE'],
            opp_r=row['oR'],
            opp_cut=row['oCut'],
            opp_bd=row['oBD'],
            opp_mr=row['oMR'],
            opp_nf2=row['oNF2'],
            opp_nf4=row['oNF4'],
            opp_caution=row['oCaution'],
            opp_tv=row['oTV'],
            opp_rt=row['oRT'],
            hi_rate=row['HIrate'],
            ho_rate=row['HOrate'],
            d_rate=row['Drate'],
            ls_rate=row['LSrate'],
            gb_rate=row['GBrate'],
            t_rate=row['Trate'],
            td_rate=row['TDrate'],
            e_rate=row['Erate'],
            ride_rate=row['Riderate'],
            apm=row['APM'],
            vs=row['VS'],
            opp_hi_rate=row['oHIrate'],
            opp_ho_rate=row['oHOrate'],
            opp_d_rate=row['oDrate'],
            opp_ls_rate=row['oLSrate'],
            opp_gb_rate=row['oGBrate'],
            opp_t_rate=row['oTrate'],
            opp_td_rate=row['oTDrate'],
            opp_e_rate=row['oErate'],
            opp_ride_rate=row['oRiderate'],
            opp_apm=row['oAPM'],
            opp_vs=row['oVS'],
            )
        p.save()

Matchdata.objects.filter(matchID__endswith='_').delete()

print(time.perf_counter())


# timeseries table, delete and rewrite
print('Stage 3')
Timeseries.objects.all().delete()

with open('C:\\Users\HotRod\wrestling_app\collector_files\match_timeseries.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        p = Timeseries(
            matchID=Matchdata.objects.get(matchID=row['matchID']),
            event_num=row['Event_Number'],
            event_lab=row['Event_Label'],
            event_time=row['Event_Time'],
            blue=row['Blue'],
            red=row['Red']
            )
        p.save()

print(time.perf_counter())
