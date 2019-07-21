import pandas as pd


# effective counter rate
def effective_counter_rate():
    wrestler = input("Enter wrestler name: ")
    matches = pd.read_csv('collection/stats/matchdata.csv', engine='python')
    ts_df = pd.read_csv('collection/stats/timeseries.csv', engine='python')
    matches = matches[matches['Focus'] == wrestler]
    matchlist = matches.MatchID.tolist()
    bluematches = [i[:4] for i in matchlist]
    redmatches = [i for i in matchlist if len(i) > 4]
    blue_ts = ts_df[ts_df['matchID_id'].isin(bluematches)]
    red_ts = ts_df[ts_df['matchID_id'].isin(redmatches)]
    bluelabels = blue_ts.event_lab.tolist()
    redlabels = red_ts.event_lab.tolist()
    bluecounter_att = 0
    bluecounter_conv = 0
    redcounter_att = 0
    redcounter_conv = 0
    for i, l in enumerate(bluelabels):
        if l == 'bgba':
            bluecounter_att += 1
            if bluelabels[i+1] == 'bexposure' or bluelabels[i+1] == 'bgbc':
                bluecounter_conv += 1
    for i, l in enumerate(redlabels):
        if l == 'rgba':
            redcounter_att += 1
            if redlabels[i+1] == 'rexposure' or redlabels[i+1] == 'rgbc':
                redcounter_conv += 1

    counter_att = bluecounter_att + redcounter_att
    counter_conv = bluecounter_conv + redcounter_conv
    counter_rate = counter_conv / counter_att
    print(matches.GBc2.sum(), matches.GBa.sum())
    print("LONG Go Behind Rate: " + str(round((matches.GBc2.sum() / matches.GBa.sum()) * 100, 2)) + "%")
    print("Go Behind Rate: " + str(round(matches.GBrate.mean(), 2)) + "%")
    return "Effective Counter Rate: " + str(round(counter_rate * 100, 2)) + "%"


if __name__ == '__main__':
    print(effective_counter_rate())
