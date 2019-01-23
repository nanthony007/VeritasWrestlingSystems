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
            blue=Wrestler.objects.get(name=row['BlueWrestler']),
            blue_team=Team.objects.get(name=row['BlueTeam']),
            red=Wrestler.objects.get(name=row['RedWrestler']),
            red_team=Team.objects.get(name=row['RedTeam']),
            blue_score=row['BluePoints'],
            red_score=row['RedPoints'],
            result=row['Result'],
            weight=row['Weight'],
            mov=row['MoV'],
            duration=row['Time'],
            blue_hia=row['blue_HIa'],
            blue_hic=row['blue_HIc'],
            blue_hoa=row['blue_HOa'],
            blue_hoc=row['blue_HOc'],
            blue_da=row['blue_Da'],
            blue_dc=row['blue_Dc'],
            blue_lsa=row['blue_LSa'],
            blue_lsc=row['blue_LSc'],
            blue_gba=row['blue_GBa'],
            blue_gbc=row['blue_GBc'],
            blue_ta=row['blue_Ta'],
            blue_tc=row['blue_Tc'],
            blue_su=row['blue_SU'],
            blue_e=row['blue_E'],
            blue_r=row['blue_R'],
            blue_cut=row['blue_Cut'],
            blue_bd=row['blue_BD'],
            blue_mr=row['blue_MR'],
            blue_nf2=row['blue_NF2'],
            blue_nf4=row['blue_NF4'],
            blue_caution=row['blue_Caution'],
            blue_tv=row['blue_TV'],
            blue_rt=row['blue_RT'],
            red_hia=row['red_HIa'],
            red_hic=row['red_HIc'],
            red_hoa=row['red_HOa'],
            red_hoc=row['red_HOc'],
            red_da=row['red_Da'],
            red_dc=row['red_Dc'],
            red_lsa=row['red_LSa'],
            red_lsc=row['red_LSc'],
            red_gba=row['red_GBa'],
            red_gbc=row['red_GBc'],
            red_ta=row['red_Ta'],
            red_tc=row['red_Tc'],
            red_su=row['red_SU'],
            red_e=row['red_E'],
            red_r=row['red_R'],
            red_cut=row['red_Cut'],
            red_bd=row['red_BD'],
            red_mr=row['red_MR'],
            red_nf2=row['red_NF2'],
            red_nf4=row['red_NF4'],
            red_caution=row['red_Caution'],
            red_tv=row['red_TV'],
            red_rt=row['red_RT'],
            blue_hi_rate=row['blue_HIrate'],
            blue_ho_rate=row['blue_HOrate'],
            blue_d_rate=row['blue_Drate'],
            blue_ls_rate=row['blue_LSrate'],
            blue_gb_rate=row['blue_GBrate'],
            blue_t_rate=row['blue_Trate'],
            blue_td_rate=row['blue_TDrate'],
            blue_e_rate=row['blue_Erate'],
            blue_ride_rate=row['blue_Riderate'],
            blue_apm=row['blue_APM'],
            blue_vs=row['blue_VS'],
            red_hi_rate=row['red_HIrate'],
            red_ho_rate=row['red_HOrate'],
            red_d_rate=row['red_Drate'],
            red_ls_rate=row['red_LSrate'],
            red_gb_rate=row['red_GBrate'],
            red_t_rate=row['red_Trate'],
            red_td_rate=row['red_TDrate'],
            red_e_rate=row['red_Erate'],
            red_ride_rate=row['red_Riderate'],
            red_apm=row['red_APM'],
            red_vs=row['red_VS'],
            )
        p.save()

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
