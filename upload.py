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
#    obj.slug = slugify(obj.abbreviation)
#    obj.save()

#print(time.perf_counter())


# wrestlers table, delete and rewrite
#print('Stage 1')
#Wrestler.objects.all().delete()

#with open('C:\\Users\HotRod\wrestling_app\collector_files\wrestlers.csv') as f:
#    reader = csv.DictReader(f)
#    for row in reader:
#        p = Wrestler(
#            name=row['WrestlerName'],
#            team=Team.objects.get(name=row['Team']),
#            eligibility=row['Eligibility'],
#            rating=row['EloRating'],
#            competitions=row['Matches'],
#            )
#        p.save()

#for obj in Wrestler.objects.all():
#    obj.slug = slugify(obj.name)
#    obj.save()

#print(time.perf_counter())


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
            result=row['Result']
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
