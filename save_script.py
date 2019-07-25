import pandas as pd
import os
import numpy as np
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()
from vws_main.models import FS_Wrestler, FS_Match, FS_TS, FS_Event
pd.options.mode.chained_assignment = None


def savecsv():
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
    def find_result_types(row):
        if row == 'WinF':
            return 'Fall'
        elif row == 'WinTF':
            return 'Tech'
        elif row == 'WinD':
            return 'Decision'
        elif row == 'LossD':
            return 'Decision'
        elif row == 'LossTF':
            return 'Tech'
        elif row == 'LossF':
            return 'Fall'

    rawcolumns = ['APM', 'Drate', 'Da', 'Date', 'Dc2', 'Dc4', 'Duration',
        'Exposure', 'Focus', 'FocusPoints', 'FocusTeam', 'GBrate', 'GBa', 'GBc2',
        'Gut', 'HIrate', 'HIa', 'HIc2', 'HIc4', 'HOrate', 'HOa', 'HOc2', 'HOc4',
        'LegLace', 'LSrate', 'LSa', 'LSc2', 'LSc4', 'MatchID', 'MoV', 'NPF', 'oAPM',
        'oDrate', 'oDa', 'oDc2', 'oDc4', 'oExposure', 'oGBrate', 'oGBa', 'oGBc2',
        'oGut', 'oHIrate', 'oHIa', 'oHIc2', 'oHIc4', 'oHOrate', 'oHOa', 'oHOc2', 'oHOc4',
        'oLegLace', 'oLSrate', 'oLSa', 'oLSc2', 'oLSc4', 'oNPF', 'oPassive',
        'oPushout', 'oRecovery', 'OppPoints', 'oTrate', 'oTa', 'oTc2', 'oTc4',
        'OppTeam', 'oTurn', 'oViolation', 'oVS', 'Opponent', 'Passive', 'Pushout',
        'Recovery', 'Result', 'Trate', 'Ta', 'Tc2', 'Tc4', 'Turn', 'Violation', 'VS',
        'Weight']

    matches = FS_Match.objects.values()
    match_df = pd.DataFrame(list(matches))
    match_df.columns = rawcolumns
    ss = []
    for i in match_df['Duration']:
        m, s, ds = i.split(':')
        t = int(m)*60 + int(s) + int(ds)/100
        ss.append(t)
    match_df['Duration'] = ss
    match_df['PassiveDiff'] = match_df.apply(lambda x: x.Passive-x.oPassive, axis=1)
    conditions = [match_df.Result=='WinF', match_df.Result=='WinTF', match_df.Result=='WinD',
        match_df.Result=='LossD', match_df.Result=='Loss TF', match_df.Result=='LossF']
    choices = [1.75, 1.50, 1.10, 0.90, 0.50, 0.25]
    match_df['NumResult'] = np.select(conditions, choices)
    match_df['BinaryResult'] = [1 if row > 1 else 0 for row in match_df.NumResult.values]
    match_df['BinaryResultText'] = ['Win' if row > 1 else 'Loss' for row in match_df.NumResult.values]
    match_df['ResultType'] = [find_result_types(row) for row in match_df.Result.values]

    # then events
    events = FS_Event.objects.values()
    events_df = pd.DataFrame(list(events))

    # wrestlers last
    wrestlers = FS_Wrestler.objects.values('name', 'team_id', 'rating')
    wrestlers_df = pd.DataFrame(list(wrestlers))
    # calculates effective wins and assigns row-wise
    for person in match_df.Focus.unique():
        group = match_df[match_df['Focus']==person]
        ew = group.NumResult.mean() * len(group.index)
        for i, row in wrestlers_df.iterrows():
            if row['name'] == person:
                wrestlers_df.at[i, 'ew'] = round(ew, 2)


    # write dataframes to csv files
    ts_df.to_csv('collection/stats/timeseries.csv', index=False)
    match_df.to_csv('collection/stats/matchdata.csv', index=False)
    events_df.to_csv('collection/stats/events.csv', index=False)
    wrestlers_df.to_csv('collection/stats/wrestlers.csv', index=False)

    return
