import csv
from vws_main.models import Wrestler, Timeseries

# wrestlers table, delete and rewrite
Wrestler.objects.all().delete()

with open('C:\\Users\HotRod\wrestling_app\collector_files\wrestlers.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        p = Wrestler(
            athlete=row['WrestlerName'],
            team=row['Team'],
            eligibility=row['Eligibility'],
            rating=row['EloRating']
            )
        p.save()


# timeseries table, delete and rewrite
Timeseries.objects.all().delete()

with open('C:\\Users\HotRod\wrestling_app\collector_files\match_timeseries.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        p = Timeseries(
            matchID=row['matchID'],
            event_num=row['Event_Number'],
            event_lab=row['Event_Label'],
            event_time=row['Event_Time'],
            blue=row['Blue'],
            red=row['Red']
            )
        p.save()
