import pandas as pd
import os
import numpy as np
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()
from vws_main.models import FS_Wrestler, FS_Match, FS_TS, FS_Event
pd.options.mode.chained_assignment = None

"""
This script extracts an instance of the database at runtime. 
It transforms the data into a consumable medium and saves it as a csv file.
Most data transformations will occur here while data filtering/cleaning will occur at the analysis stage.
This is done to simplify and expedite analysis documents so they do not require loading django each runtime.

"""

# timeseries first
ts = FS_TS.objects.values()
ts_df = pd.DataFrame(list(ts))
# remove useless id column
ts_df = ts_df.drop(columns=['id'])
ts_df = ts_df[ts_df['matchID_id'].str.len()==4]
# reassign time value to fractional seconds not string
tt = []
for i in ts_df['event_time']:
    m, s, ds = i.split(':')
    t = int(m)*60 + int(s) + int(ds)/100
    tt.append(t)
ts_df['event_time'] = tt
ts_df = ts_df.sort_values(['matchID_id', 'event_num'])
ts_df.reset_index(drop=True, inplace=True)

# matches next
matches = FS_Match.objects.values()
match_df = pd.DataFrame(list(matches))
ss = []
for i in match_df['duration']:
    m, s, ds = i.split(':')
    t = int(m)*60 + int(s) + int(ds)/100
    ss.append(t)
match_df['duration'] = ss
match_df['passive_dif'] = match_df.apply(lambda x: x.passive-x.opp_passive, axis=1)
conditions = [match_df.result=='WinF', match_df.result=='WinTF', match_df.result=='WinD',
    match_df.result=='LossD', match_df.result=='Loss TF', match_df.result=='LossF']
choices = [1.75, 1.50, 1.10, 0.90, 0.50, 0.25]
match_df['num_result'] = np.select(conditions, choices)

# then events
events = FS_Event.objects.values()
events_df = pd.DataFrame(list(events))

# wrestlers last
wrestlers = FS_Wrestler.objects.values('name', 'team_id', 'rating')
wrestlers_df = pd.DataFrame(list(wrestlers))

# write dataframes to csv files
ts_df.to_csv('collection/stats/timeseries.csv', index=False)
match_df.to_csv('collection/stats/matchdata.csv', index=False)
events_df.to_csv('collection/stats/events.csv', index=False)
wrestlers_df.to_csv('collection/stats/wrestlers.csv', index=False)
