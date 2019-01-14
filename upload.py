import csv, time
from vws_main.models import Wrestler, Timeseries, Matchdata

# wrestlers table, delete and rewrite
print('Stage 1')
Wrestler.objects.all().delete()

with open('C:\\Users\HotRod\wrestling_app\collector_files\wrestlers.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        p = Wrestler(
            name=row['WrestlerName'],
            team=row['Team'],
            eligibility=row['Eligibility'],
            rating=row['EloRating'],
            competitions=row['Matches']
            )
        p.save()

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
            blue=row['BlueWrestler'],
            red=row['RedWrestler'],
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
