import pandas as pd


# safe division
def safe_div(x, y):
    """
    Accepts two numeric parameters.
    Safely divide first by second, even if second value is zero.
    """
    if y == 0:
        return x / (y + 1)
    else:
        return x / y



# effective counter rate
def effective_counter_rate(x_wrestler):
    matches = pd.read_csv('collection/stats/matchdata.csv', engine='python')
    ts_df = pd.read_csv('collection/stats/timeseries.csv', engine='python')
    matches = matches[matches['Focus'] == x_wrestler]
    matchlist = matches.MatchID.tolist()
    bluematches = [i[:4] for i in matchlist]
    redmatches = [i for i in matchlist if len(i) > 4]
    blue_ts = ts_df[ts_df['matchID_id'].isin(bluematches)]
    red_ts = ts_df[ts_df['matchID_id'].isin(redmatches)]
    bluelabels = blue_ts.event_lab.tolist()
    redlabels = red_ts.event_lab.tolist()
    counter_att = 0
    counter_conv = 0
    opp_counter_att = 0
    opp_counter_conv = 0

    # get focus nums
    for i, l in enumerate(bluelabels):
        if (i + 1) == len(bluelabels):
            pass
        if l == 'bgba':
            counter_att += 1
            if bluelabels[i+1] == 'bexposure' or bluelabels[i+1] == 'bgbc':
                counter_conv += 1
    for i, l in enumerate(redlabels):
        if (i + 1) == len(redlabels):
            pass
        if l == 'rgba':
            counter_att += 1
            if redlabels[i+1] == 'rexposure' or redlabels[i+1] == 'rgbc':
                counter_conv += 1
    # get opp nums
    for i, l in enumerate(bluelabels):
        if (i + 1) == len(bluelabels):
            pass
        if l == 'rgba':
            opp_counter_att += 1
            if bluelabels[i + 1] == 'rexposure' or bluelabels[i + 1] == 'rgbc':
                opp_counter_conv += 1

    for i, l in enumerate(redlabels):
        if (i + 1) == len(redlabels):
            pass
        if l == 'bgba':
            opp_counter_att += 1
            if redlabels[i+1] == 'bexposure' or redlabels[i+1] == 'bgbc':
                opp_counter_conv += 1

    counter_rate = (counter_conv / counter_att) * 100
    opp_counter_rate = (opp_counter_conv / opp_counter_att) * 100
    # print(matches.GBc2.sum(), matches.GBa.sum())
    # print("LONG Go Behind Rate: " + str(round((matches.GBc2.sum() / matches.GBa.sum()) * 100, 2)) + "%")
    # print("Go Behind Rate: " + str(round(matches.GBrate.mean(), 2)) + "%")
    # print("Go Behind Rate: " + str(round(counter_rate, 2)) + "%")
    # print("OPP Go Behind Rate: " + str(round(opp_counter_rate, 2)) + "%")
    return counter_rate, opp_counter_rate

