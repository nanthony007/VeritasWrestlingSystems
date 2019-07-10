import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from django.http import HttpResponse
import seaborn as sns
import os
import io


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


def graph(first, last):
    f = str(first)
    l = str(last)
    cwd = os.getcwd()
    matches = pd.read_csv(cwd+'/collection/stats/matchdata.csv', engine='python')
    matches = matches[matches.focus_id == f + ' ' + l]
    #calculations
    HIC = matches.hia.sum()
    HOC = matches.hoa.sum()
    DC = matches.da.sum()
    LSC = matches.lsa.sum()
    GBC = matches.gba.sum()
    TC = matches.ta.sum()
    totalTDA = matches.hia.sum() + matches.hoa.sum() + matches.da.sum() + matches.lsa.sum() + matches.gba.sum() + matches.ta.sum()
    oHIC = matches.opp_hia.sum()
    oHOC = matches.opp_hoa.sum()
    oDC = matches.opp_da.sum()
    oLSC = matches.opp_lsa.sum()
    oGBC = matches.opp_gba.sum()
    oTC = matches.opp_ta.sum()
    ototalTDA = matches.opp_hia.sum() + matches.opp_hoa.sum() + matches.opp_da.sum() + matches.opp_lsa.sum() + matches.opp_gba.sum() + matches.opp_ta.sum()
    # sets up dataframes
    shot_labels = ['Head Inside', 'Head Outside', 'Double', 'LowShot', 'Counter', 'Throw',
                   'Head Inside', 'Head Outside', 'Double', 'LowShot', 'Counter', 'Throw']
    athlete = ['Focus', 'Focus', 'Focus', 'Focus', 'Focus', 'Focus',
               'Opponent', 'Opponent', 'Opponent', 'Opponent', 'Opponent', 'Opponent']
    rates = [matches.hi_rate.mean(), matches.ho_rate.mean(), matches.d_rate.mean(), matches.ls_rate.mean(), matches.gb_rate.mean(),
             matches.t_rate.mean(),
             matches.opp_hi_rate.mean(), matches.opp_ho_rate.mean(), matches.opp_d_rate.mean(), matches.opp_ls_rate.mean(),
             matches.gb_rate.mean(), matches.opp_t_rate.mean()]
    prefs = [(HIC / totalTDA) * 100, (HOC / totalTDA) * 100, (DC / totalTDA) * 100, (LSC / totalTDA) * 100,
             (GBC / totalTDA) * 100, (TC / totalTDA) * 100,
             (oHIC / ototalTDA) * 100, (oHOC / ototalTDA) * 100, (oDC / ototalTDA) * 100, (oLSC / ototalTDA) * 100,
             (oGBC / ototalTDA) * 100, (oTC / ototalTDA) * 100]
    rate_df = pd.DataFrame()
    rate_df['wrestler'] = athlete
    rate_df['shottype'] = shot_labels
    rate_df['rate'] = rates
    rate_df['pref'] = prefs
    matches2 = pd.melt(matches, id_vars=['binary_result'], value_vars=['npf'])

    #correlations
    matches_inter = matches.select_dtypes(exclude=['object'])
    matches_inter = matches_inter.drop(columns=['mov', 'focus_score', 'opp_score', 'num_result'])
    corrs = matches_inter.corr()['binary_result'][:-1].dropna()
    corrs = corrs[corrs > -1]
    corrs = corrs[corrs < 1]
    bad = corrs.sort_values(ascending=True)[:10]
    good = corrs.sort_values(ascending=False)[:10]

    #plot
    sns.set_style('white', {'axes.spines.right': False, 'axes.spines.top': False})
    fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize=(16, 9))
    plt.subplots_adjust(wspace=0.50, hspace=0.50)
    g1 = sns.countplot(y='result_type', hue='binary_result_text', data=matches, order=['', 'Fall', 'Tech', 'Decision'],
                       palette=sns.diverging_palette(240, 10, n=2), ax=ax1)
    ax1.set_title('Results')
    ax1.set_xlabel("Count")
    ax1.set_ylabel("Result Type")
    ax1.legend(loc='upper center', ncol=2, frameon=False)
    g2 = sns.lineplot(data=matches, x=range(1, len(matches.index) + 1), y='vs', ax=ax2)
    ax2.axhline(matches.vs.mean(), label='World Average', color='gold')
    ax2.set_title("Veritas Score")
    ax2.set_xlabel("Matches")
    ax2.set_ylabel("VS")
    ax2.legend(loc='upper center', frameon=False)
    ax2.legend_.set_title("")
    g3 = sns.barplot(x='pref', y='shottype', hue='wrestler', data=rate_df,
                     palette=sns.diverging_palette(240, 10, n=2), ax=ax3)
    ax3.set_title('Preference')
    ax3.set_xlabel("Preference (% of total shots)")
    ax3.set_ylabel("Shot Type")
    ax3.legend(loc='center right', frameon=False)
    ax3.legend_.set_title("")
    g4 = sns.barplot(x='rate', y='shottype', hue='wrestler', data=rate_df,
                     palette=sns.diverging_palette(240, 10, n=2), ax=ax4)
    ax4.set_title('Effeciency')
    ax4.set_xlabel("Effeciency Rate (%)")
    ax4.legend(loc="center right", frameon=False)
    ax4.legend_.set_title("")
    g5 = sns.barplot(x=good.values, y=good.index, palette=sns.light_palette("darkblue", 10, reverse=True), ax=ax5)
    ax5.set_title('Good Actions (Top 10)')
    ax5.set_xlabel("Correlation to Winning")
    ax5.set_ylabel("Action")
    g6 = sns.barplot(x=bad.values, y=bad.index, palette=sns.light_palette("crimson", 10, reverse=True), ax=ax6)
    ax6.set_title('Bad Actions (Top 10)')
    ax6.set_xlabel("Correlation to Winning")
    ax6.set_ylabel("Action")
    plt.suptitle('Wrestler Report Metrics', size=16)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    response = HttpResponse(buf.getvalue(), content_type='image/png')
    return response
