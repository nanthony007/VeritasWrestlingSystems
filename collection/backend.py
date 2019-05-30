import pandas as pd
import tkinter as tk
import inspect
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()
from vws_main.models import FS_Wrestler, FS_Match, FS_TS

K = 40

# wrestlers = pd.read_csv("collection/stats/wrestlers.csv")
# wrestlers = wrestlers.set_index('Name')


# adapted MoV for pin falls
def pins(self):
    """
    Adjust margin of victory to unrealistic/impossible value for pinfalls
    to adjust EloRating formula accordingly.
    Returns adjusted MOV.
    """
    mov = self.x.blue_score.get() - self.x.red_score.get()

    if self.x.result.get() == 'Blue Fall':
        mov = 25
    elif self.x.result.get() == 'Red Fall':
        mov = 25
    return mov


# ranking function using Elo system
def ranking_function(self):
    """
    EloRating rating formula adjuster.
    Takes match_id variable of Events class instance as paramter.
    Calculates and saves new ratings in database.
    Returns nothing.
    """
    Ra1 = FS_Wrestler.objects.get(name=self.controller.shared_data['blue_name'].get())
    Rb1 = FS_Wrestler.objects.get(name=self.controller.shared_data['red_name'].get())

    Ra = Ra1.rating
    Rb = Rb1.rating

    # sets binary result
    Sa = 0
    if self.x.result.get() == 'Blue Fall':
        Sa = 1
    elif self.x.result.get() == 'Blue Technical Fall':
        Sa = 1
    elif self.x.result.get() == 'Blue Major Decision':
        Sa = 1
    elif self.x.result.get() == 'Blue Decision':
        Sa = 1
    elif self.x.result.get() == 'Red Decision':
        Sa = 0
    elif self.x.result.get() == 'Red Major Decision':
        Sa = 0
    elif self.x.result.get() == 'Red Technical Fall':
        Sa = 0
    elif self.x.result.get() == 'Red Fall':
        Sa = 0

    elo_dif = Ra - Rb

    Ea = 1 / (1 + 10 ** ((Rb - Ra) / 400))
    print('Red chance to win:', round(1-Ea, 2), '\nResult:', 1-Sa)
    print('Blue chance to win:', round(Ea, 2), '\nResult:', Sa)
    self.textbox.insert(tk.END, 'Red chance to win: ' + str(round(1-Ea, 2)) + '\n', 'center-tag')
    self.textbox.insert(tk.END, 'Blue chance to win: ' + str(round(Ea, 2)) + '\n', 'center-tag')

    potential = K * (Sa - Ea)

    factor = ((abs(pins(self)) + 3) ** 0.8) / (7.5 + (0.006 * elo_dif))
    change = factor * potential
    print('Change: ', abs(round(change, 0)))
    self.textbox.insert(tk.END, 'Change: ' + str(abs(round(change, 0))) + '\n','center-tag')

    nRa = round(Ra + change, 0)
    #wrestlers.Rating[self.controller.shared_data['blue_name'].get()] = int(nRa)
    Ra1.rating = int(nRa)
    Ra1.save()
    nRb = round(Rb - change, 0)
    #wrestlers.Rating[self.controller.shared_data['red_name'].get()] = int(nRb)
    Rb1.rating = int(nRb)
    Rb1.save()

    print('New Red Rating =', round(nRb, 0))
    print('New Blue Rating =', round(nRa, 0))
    self.textbox.insert(tk.END, 'New Red Rating = ' + str(round(nRb, 0)) + '\n', 'center-tag')
    self.textbox.insert(tk.END, 'New Blue Rating = ' + str(round(nRa, 0)) + '\n', 'center-tag')
    self.textbox.configure(state=tk.DISABLED)
    #wrestlers.to_csv("collection\stats\\wrestlers.csv", mode="w")
    return


# allows two functions
def combine_funcs(*funcs):
    """
    Allows use of two functions inside one button call.
    Takes functions as parameters.
    """
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func


# numeric result calculator, provides string version of result for display in tables
def num_result(self):
    """
    Gets result of match from user.
    Input should be CamelCase with spaces following Recording procedures.
    Saves result as numeric value for red/blue instances of Match.
    Returns Result abbreviation and saves opposite abbreviation for oppponent.
    """
    if self.result.get() == 'Blue Fall':
        self.b_result.set(1.75)
        self.r_result.set(0.25)
        self.result_abb.set('WinF')
        self.result_opp_abb.set('LossF')
    elif self.result.get() == 'Blue Technical Fall':
        self.b_result.set(1.25)
        self.r_result.set(0.50)
        self.result_abb.set('WinTF')
        self.result_opp_abb.set('LossTF')
    elif self.result.get() == 'Blue Decision':
        self.b_result.set(1.25)
        self.r_result.set(0.75)
        self.result_abb.set('WinD')
        self.result_opp_abb.set('LossD')
    elif self.result.get() == 'Red Decision':
        self.b_result.set(0.75)
        self.r_result.set(1.25)
        self.result_abb.set('LossD')
        self.result_opp_abb.set('WinD')
    elif self.result.get() == 'Red Technical Fall':
        self.b_result.set(0.50)
        self.r_result.set(1.50)
        self.result_abb.set('LossTF')
        self.result_opp_abb.set('WinTF')
    elif self.result.get() == 'Red Fall':
        self.b_result.set(0.25)
        self.r_result.set(1.75)
        self.result_abb.set('LossF')
        self.result_opp_abb.set('WinF')



"""
The following functions are used in buttons on the MatchPage.
Each button increametns its value by one, appends a row to the TS dataframe,
adds a new FS_TS instance for each Match, and redraws the displayed table.
"""

# blue and red button functions
def bhia(self):
    self.bhia += 1
    datatemp = pd.DataFrame(
        {'EventNum': self.event_lab.get() + 1,
        'EventLabel': inspect.stack()[0][3],
        'EventTime': self.main_clock.timestr.get(),
        'Blue': self.blue_score.get(),
        'Red': self.red_score.get(),
        'matchID': self.matchID_value},
        index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat(
        [datatemp.drop(['Blue', 'Red', 'matchID'], axis=1),
        self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.bhia)


def bhoa(self):
    self.bhoa += 1
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.bhoa)


def bda(self):
    self.bda += 1
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.bda)


def blsa(self):
    self.blsa += 1
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.blsa)


def bgba(self):
    self.bgba += 1
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.bgba)


def bta(self):
    self.bta += 1
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.bta)


def bhic2(self):
    self.bhic2 += 1
    self.blue_score.set(self.blue_score.get() + 2)
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.bhic2)


def bhic4(self):
    self.bhic4 += 1
    self.blue_score.set(self.blue_score.get() + 4)
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.bhic4)


def bhoc2(self):
    self.bhoc2 += 1
    self.blue_score.set(self.blue_score.get() + 2)
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.bhoc2)


def bhoc4(self):
    self.bhoc4 += 1
    self.blue_score.set(self.blue_score.get() + 4)
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.bhoc4)


def bdc2(self):
    self.bdc2 += 1
    self.blue_score.set(self.blue_score.get() + 2)
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.bdc2)


def bdc4(self):
    self.bdc4 += 1
    self.blue_score.set(self.blue_score.get() + 4)
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.bdc4)


def blsc2(self):
    self.blsc2 += 1
    self.blue_score.set(self.blue_score.get() + 2)
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.blsc2)


def blsc4(self):
    self.blsc4 += 1
    self.blue_score.set(self.blue_score.get() + 4)
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.blsc4)


def bgbc(self):
    self.bgbc += 1
    self.blue_score.set(self.blue_score.get() + 2)
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.bgbc)


def btc2(self):
    self.btc2 += 1
    self.blue_score.set(self.blue_score.get() + 2)
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.btc2)


def btc4(self):
    self.btc4 += 1
    self.blue_score.set(self.blue_score.get() + 4)
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.btc4)


def bexposure(self):
    self.bexposure += 1
    self.blue_score.set(self.blue_score.get() + 2)
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.bexposure)


def bgut(self):
    self.bgut += 1
    self.blue_score.set(self.blue_score.get() + 2)
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.bgut)


def bleglace(self):
    self.bleglace += 1
    self.blue_score.set(self.blue_score.get() + 2)
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.bleglace)


def bturn(self):
    self.bturn += 1
    self.blue_score.set(self.blue_score.get() + 2)
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.bturn)


def brecovery(self):
    self.brecovery += 1
    self.blue_score.set(self.blue_score.get() + 1)
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.brecovery)


def bpushout(self):
    self.bpushout += 1
    self.blue_score.set(self.blue_score.get() + 1)
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.bpushout)


def bpassive(self):
    self.bpassive += 1
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.bpassive)


def btv1(self):
    self.btv += 1
    self.red_score.set(self.red_score.get() + 1)
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.btv)


def btv2(self):
    self.btv += 1
    self.red_score.set(self.red_score.get() + 2)
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.btv)


def rhia(self):
    self.rhia += 1
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.rhia)


def rhoa(self):
    self.rhoa += 1
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.rhoa)


def rda(self):
    self.rda += 1
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.rda)


def rlsa(self):
    self.rlsa += 1
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.rlsa)


def rgba(self):
    self.rgba += 1
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.rgba)


def rta(self):
    self.rta += 1
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.rta)


def rhic2(self):
    self.rhic2 += 1
    self.red_score.set(self.red_score.get() + 2)
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.rhic2)


def rhic4(self):
    self.rhic4 += 1
    self.red_score.set(self.red_score.get() + 4)
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.rhic4)


def rhoc2(self):
    self.rhoc2 += 1
    self.red_score.set(self.red_score.get() + 2)
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.rhoc2)


def rhoc4(self):
    self.rhoc4 += 1
    self.red_score.set(self.red_score.get() + 4)
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.rhoc4)


def rdc2(self):
    self.rdc2 += 1
    self.red_score.set(self.red_score.get() + 2)
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.rdc2)


def rdc4(self):
    self.rdc4 += 1
    self.red_score.set(self.red_score.get() + 4)
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.rdc4)


def rlsc2(self):
    self.rlsc2 += 1
    self.red_score.set(self.red_score.get() + 2)
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.rlsc2)


def rlsc4(self):
    self.rlsc4 += 1
    self.red_score.set(self.red_score.get() + 4)
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.rlsc4)


def rgbc(self):
    self.rgbc += 1
    self.red_score.set(self.red_score.get() + 2)
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.rgbc)


def rtc2(self):
    self.rtc2 += 1
    self.red_score.set(self.red_score.get() + 2)
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.btc2)


def rtc4(self):
    self.rtc4 += 1
    self.red_score.set(self.red_score.get() + 4)
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.rtc4)


def rexposure(self):
    self.rexposure += 1
    self.red_score.set(self.red_score.get() + 2)
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.rexposure)


def rgut(self):
    self.rgut += 1
    self.red_score.set(self.red_score.get() + 2)
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.rgut)


def rleglace(self):
    self.rleglace += 1
    self.red_score.set(self.red_score.get() + 2)
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.rleglace)


def rturn(self):
    self.rturn += 1
    self.red_score.set(self.red_score.get() + 2)
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.rturn)


def rrecovery(self):
    self.rrecovery += 1
    self.red_score.set(self.red_score.get() + 1)
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.rrecovery)


def rpushout(self):
    self.rpushout += 1
    self.red_score.set(self.red_score.get() + 1)
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.rpushout)


def rpassive(self):
    self.rpassive += 1
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.rpassive)


def rtv1(self):
    self.rtv += 1
    self.blue_score.set(self.blue_score.get() + 1)
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.rtv)


def rtv2(self):
    self.rtv += 1
    self.blue_score.set(self.blue_score.get() + 2)
    datatemp = pd.DataFrame({'EventNum': self.event_lab.get() + 1, 'EventLabel': inspect.stack()[0][3], 'EventTime': self.main_clock.timestr.get(), 'Blue': self.blue_score.get(), 'Red': self.red_score.get(), 'matchID': self.matchID_value}, index=[0])
    ts1 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts2 = FS_TS(
        matchID=FS_Match.objects.get(matchID=self.matchID_value + '*'),
        event_num=self.event_lab.get() + 1,
        event_lab=inspect.stack()[0][3],
        event_time=self.main_clock.timestr.get(),
        blue=self.blue_score.get(),
        red=self.red_score.get()
    )
    ts1.save()
    ts2.save()
    self.event_lab.set(self.event_lab.get() + 1)
    self.ts_df = self.ts_df.append(datatemp, ignore_index=True)
    self.display_df = pd.concat([datatemp.drop(['Blue', 'Red', 'matchID'], axis=1), self.display_df.iloc[:]]).reset_index(drop=True)
    self.pbp.model.df = self.display_df
    self.pbp.redraw()
    print(self.rtv)
