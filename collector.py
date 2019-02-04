# import modules
import pandas as pd
import time
import datetime
import string
import random
from sqlalchemy import create_engine
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django
django.setup()
from vws_main.models import Wrestler, Matchdata, Timeseries

pd.options.mode.chained_assignment = None

seconds = 1

K = 40

# safe division
def safe_div(x, y):
    if y == 0:
        return x / (y + 1)
    else:
        return x / y


class ColorData(object):

    def __init__(self):
        self.weight = None
        self.result = 0
        self.head_inside_attempt = 0
        self.head_inside_conversion = 0
        self.head_outside_attempt = 0
        self.head_outside_conversion = 0
        self.double_attempt = 0
        self.double_conversion = 0
        self.low_shot_attempt = 0
        self.low_shot_conversion = 0
        self.go_behind_attempt = 0
        self.go_behind_conversion = 0
        self.throw_attempt = 0
        self.throw_conversion = 0
        self.stand_up = 0
        self.escape = 0
        self.reversal = 0
        self.cut = 0
        self.breakdown = 0
        self.mat_return = 0
        self.near_fall_2 = 0
        self.near_fall_4 = 0
        self.stalling = 0
        self.caution = 0
        self.technical_violation = 0
        self.riding_time = 0
        self.first_choice = None
        self.second_choice = None
        self.bottom_chances = 0
        self.top_chances = 0

    def comp(self):
        head_inside_rate = safe_div(self.head_inside_conversion, self.head_inside_attempt)
        head_outside_rate = safe_div(self.head_outside_conversion, self.head_outside_attempt)
        double_rate = safe_div(self.double_conversion, self.double_attempt)
        low_shot_rate = safe_div(self.low_shot_conversion, self.low_shot_attempt)
        go_behind_rate = safe_div(self.go_behind_conversion, self.go_behind_attempt)
        throw_rate = safe_div(self.throw_conversion, self.throw_attempt)
        td_rate = safe_div((self.head_inside_conversion + self.head_outside_conversion + self.double_conversion + self.low_shot_conversion + self.go_behind_conversion + self.throw_conversion),
                           (self.head_inside_attempt + self.head_outside_attempt + self.double_attempt + self.low_shot_attempt + self.go_behind_attempt + self.throw_attempt))
        tda = self.head_inside_attempt + self.head_outside_attempt + self.double_attempt + self.low_shot_attempt + self.go_behind_attempt + self.throw_attempt
        tdc = self.head_inside_conversion + self.head_outside_conversion + self.double_conversion + self.low_shot_conversion + self.go_behind_conversion + self.throw_conversion
        return head_inside_rate, head_outside_rate, double_rate, low_shot_rate, go_behind_rate, throw_rate, td_rate, tda, tdc


class Events(ColorData):

    def __init__(self):
        super(Events, self).__init__()
        while True:
            b = input('Blue Wrestler: ')
            try:
                w_blue = Wrestler.objects.get(name=b)
                break
            except:
                print('Wrestler not in database, please try again.')
                continue

        while True:
            r = input('Red Wrestler: ')
            try:
                w_red = Wrestler.objects.get(name=r)
                break
            except:
                print('Wrestler not in database, please try again.')
                continue

        while True:
            w = int(input('Weight Class: '))
            weight_classes = [125,133,141,149,157,165,174,184,197,285]
            if w in weight_classes:
                break
            else:
                print('Invalid weight class, please try again.')
                continue


        self.match_id =  ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        m1 = Matchdata(matchID=self.match_id)
        m1.save()
        self.blue = ColorData()
        self.red = ColorData()

        self.blue.name, self.red.name = w_blue.name, w_red.name
        self.blue.team = w_blue.team.name
        self.red.team = w_red.team.name
        self.weight = w

        self.tda = self.blue.comp()[-2] + self.red.comp()[-2]
        self.tdc = self.blue.comp()[-1] + self.red.comp()[-1]

        self.raw()
        self.opp_result = 0
        self.result = self.result_value()
        self.scores()
        self.ranking_fun(self.match_id)
        self.close_fun()


    def raw(self):

        event_num = 0
        df2 = pd.DataFrame(columns=['Event_Number', 'Event_Label', 'Event_Time'])
        print('Blue: ', self.blue.name, self.blue.team, Wrestler.objects.get(name=self.blue.name).rating, '\nRed: ', self.red.name, self.red.team, Wrestler.objects.get(name=self.red.name).rating, '\nMatch: ', self.match_id)

        while True:

            command = input('Event: ')  # start of user interaction

            # start command
            if command == 'START':
                global start
                start = time.time()
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            # choice commands
            elif command == 'first':
                color = input('Color: ')
                choice = input('Choice: ')

                if color == 'blue':
                    self.blue.first_choice = choice
                elif color == 'red':
                    self.red.first_choice = choice

                if choice == 'top':
                    self.blue.top_chances += 1
                    self.red.bottom_chances += 1
                elif choice == 'bottom':
                    self.blue.bottom_chances += 1
                    self.red.top_chances += 1
                elif choice == 'defer':
                    pass

                event_num += 1
                event_label = color.upper() + choice.upper()
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'second':
                color = input('Color: ')
                choice = input('Choice: ')
                if color == 'blue':
                    self.blue.second_choice = choice
                elif color == 'red':
                    self.red.second_choice = choice

                if choice == 'top':
                    self.red.top_chances += 1
                    self.blue.bottom_chances += 1
                elif choice == 'bottom':
                    self.red.bottom_chances += 1
                    self.blue.top_chances += 1

                event_num += 1
                event_label = color.upper() + choice.upper()
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            # start BLUE commands
            elif command == 'bhia':
                self.blue.head_inside_attempt += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'bhic':
                self.blue.head_inside_conversion += 1
                self.blue.top_chances += 1
                self.red.bottom_chances += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'bhoa':
                self.blue.head_outside_attempt += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'bhoc':
                self.blue.head_outside_conversion += 1
                self.blue.top_chances += 1
                self.red.bottom_chances += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'bda':
                self.blue.double_attempt += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'bdc':
                self.blue.double_conversion += 1
                self.blue.top_chances += 1
                self.red.bottom_chances += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'blsa':
                self.blue.low_shot_attempt += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'blsc':
                self.blue.low_shot_conversion += 1
                self.blue.top_chances += 1
                self.red.bottom_chances += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'bgba':
                self.blue.go_behind_attempt += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'bgbc':
                self.blue.go_behind_conversion += 1
                self.blue.top_chances += 1
                self.red.bottom_chances += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'bta':
                self.blue.throw_attempt += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'btc':
                self.blue.throw_conversion += 1
                self.blue.top_chances += 1
                self.red.bottom_chances += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'bsu':
                self.blue.stand_up += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'be':
                self.blue.escape += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'br':
                self.blue.reversal += 1
                self.blue.top_chances += 1
                self.red.bottom_chances += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'bc':
                self.blue.cut += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'bbd':
                self.blue.breakdown += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'bmr':
                self.blue.mat_return += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'bnf2':
                self.blue.near_fall_2 += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'bnf4':
                self.blue.near_fall_4 += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'bC':
                self.blue.caution += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'bstall':
                self.blue.stalling += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'bTV':
                self.blue.technical_violation += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'bRT':
                self.blue.riding_time += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            # start RED commands
            elif command == 'rhia':
                self.red.head_inside_attempt += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'rhic':
                self.red.head_outside_conversion += 1
                self.red.top_chances += 1
                self.blue.bottom_chances += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'rhoa':
                self.red.head_outside_attempt += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'rhoc':
                self.red.head_outside_conversion += 1
                self.red.top_chances += 1
                self.blue.bottom_chances += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'rda':
                self.red.double_attempt += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'rdc':
                self.red.double_conversion += 1
                self.red.top_chances += 1
                self.blue.bottom_chances += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'rlsa':
                self.red.low_shot_attempt += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'rlsc':
                self.red.low_shot_conversion += 1
                self.red.top_chances += 1
                self.blue.bottom_chances += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'rgba':
                self.red.go_behind_attempt += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'rgbc':
                self.red.go_behind_conversion += 1
                self.red.top_chances += 1
                self.blue.bottom_chances += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'rta':
                self.red.throw_attempt += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'rtc':
                self.red.throw_conversion += 1
                self.red.top_chances += 1
                self.blue.bottom_chances += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'rsu':
                self.red.stand_up += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 're':
                self.red.escape += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'rr':
                self.red.reversal += 1
                self.red.top_chances += 1
                self.blue.bottom_chances += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'rc':
                self.red.cut += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'rbd':
                self.red.breakdown += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'rmr':
                self.red.mat_return += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'rnf2':
                self.red.near_fall_2 += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'rnf4':
                self.red.near_fall_4 += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'rC':
                self.red.caution += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'rstall':
                self.red.stalling += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'rTV':
                self.red.technical_violation += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            elif command == 'rRT':
                self.red.riding_time += 1
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

            # end command
            elif command == 'END':
                event_num += 1
                event_label = command
                event_time = round((time.time()-start), 2)

                global seconds
                seconds = round((time.time()-start), 2)

                ts = Timeseries(matchID=Matchdata.objects.get(matchID=self.match_id), event_num=event_num, event_lab=event_label, event_time=event_time, blue=self.scores()[0], red=self.scores()[1])
                ts.save()
                datatemp = {'Event_Number': event_num, 'Event_Label': event_label, 'Event_Time': event_time, 'Blue': self.scores()[0], 'Red': self.scores()[1]}
                df2 = df2.append(datatemp, ignore_index=True)
                print(df2)

                global match_timeseries
                match_timeseries = df2
                return

            else:
                print('Invalid command, try again')

    def result_value(self):
        value = str(input('Result: '))
        if value == 'blue fall':
            self.blue.result = 1.75
            self.red.result = 0.25
            zz = 'WinF'
            self.opp_result = 'LossF'
        elif value == 'blue tech':
            self.blue.result = 1.50
            self.red.result = 0.50
            zz = 'WinTF'
            self.opp_result = 'LossTF'
        elif value == 'blue major':
            self.blue.result = 1.25
            self.red.result = 0.75
            zz = 'WinMD'
            self.opp_result = 'LossMD'
        elif value == 'blue decision':
            self.blue.result = 1.10
            self.red.result = 0.90
            zz = 'WinD'
            self.opp_result = 'LossD'
        elif value == 'red decision':
            self.blue.result = 0.90
            self.red.result = 1.10
            zz = 'LossD'
            self.opp_result = 'WinD'
        elif value == 'red major':
            self.blue.result = 0.75
            self.red.result = 1.25
            zz = 'LossMD'
            self.opp_result = 'WinMD'
        elif value == 'red tech':
            self.blue.result = 0.50
            self.red.result = 1.50
            zz = 'LossTF'
            self.opp_result = 'WinTF'
        elif value == 'red fall':
            self.blue.result = 0.25
            self.red.result = 1.75
            zz = 'LossF'
            self.opp_result = 'WinF'
        return zz

    def scores(self):
        blue_points = (self.blue.comp()[-1] + self.blue.reversal + self.blue.near_fall_2) * 2 + (self.blue.near_fall_4 * 4) + self.blue.escape

        if self.red.caution == 3:
            blue_points += 1
        elif self.red.caution == 4:
            blue_points += 1

        if self.red.technical_violation == 1:
            blue_points += 1
        elif self.red.technical_violation == 2:
            blue_points += 2
        elif self.red.technical_violation == 3:
            blue_points += 4

        if self.red.stalling == 2:
            blue_points += 1
        elif self.red.stalling == 3:
            blue_points += 2
        elif self.red.stalling == 4:
            blue_points += 4

        red_points = (self.red.comp()[-1] + self.red.reversal + self.red.near_fall_2) * 2 + (self.red.near_fall_4 * 4) + self.red.escape

        if self.blue.caution == 3:
            red_points += 1
        elif self.blue.caution == 4:
            red_points += 2

        if self.blue.technical_violation == 1:
            red_points += 1
        elif self.blue.technical_violation == 2:
            red_points += 2
        elif self.blue.technical_violation == 3:
            red_points += 4

        if self.blue.stalling == 2:
            red_points += 1
        elif self.blue.stalling == 3:
            red_points += 2
        elif self.blue.stalling == 4:
            red_points += 4

        blue_weighted_result = self.blue.result * (Wrestler.objects.get(name=self.red.name).rating / 100)
        red_weighted_result = self.red.result * (Wrestler.objects.get(name=self.red.name).rating / 100)

        blue_escape_rate = safe_div((self.blue.escape + self.blue.reversal), self.blue.bottom_chances)
        red_escape_rate = safe_div((self.red.escape + self.red.reversal), self.red.bottom_chances)
        blue_ride_rate = safe_div((self.red.escape + self.red.reversal), self.blue.top_chances)
        red_ride_rate = safe_div((self.blue.escape + self.blue.reversal), self.red.top_chances)

        blue_npf = safe_div((self.blue.head_inside_attempt + self.blue.head_outside_attempt + self.blue.double_attempt + self.blue.low_shot_attempt + self.blue.throw_attempt), self.tda) + safe_div(self.blue.comp()[-1], self.tdc)
        red_npf = safe_div((self.red.head_inside_attempt + self.red.head_outside_attempt + self.red.double_attempt + self.red.low_shot_attempt + self.red.throw_attempt), self.tda) + safe_div(self.red.comp()[-1], self.tdc)

        blue_apm = (self.blue.head_inside_attempt + self.blue.head_outside_attempt + self.blue.double_attempt + self.blue.low_shot_attempt + self.blue.go_behind_attempt + self.blue.throw_attempt + self.blue.escape +
                    (self.blue.head_inside_conversion + self.blue.head_outside_conversion + self.blue.double_conversion + self.blue.low_shot_conversion + self.blue.go_behind_conversion + self.blue.throw_conversion + self.blue.near_fall_2 + self.blue.reversal) * 2 + (
                            self.blue.breakdown + self.blue.mat_return + self.blue.cut + self.blue.stand_up) * 0.5 + (self.blue.near_fall_4 * 4) - self.blue.stalling) / (seconds / 60.0)
        red_apm = (self.red.head_inside_attempt + self.red.head_outside_attempt + self.red.double_attempt + self.red.low_shot_attempt + self.red.go_behind_attempt + self.red.throw_attempt + self.red.escape +
                   (self.red.head_inside_conversion + self.red.head_outside_conversion + self.red.double_conversion + self.red.low_shot_conversion + self.red.go_behind_conversion + self.red.throw_conversion + self.red.near_fall_2 + self.red.reversal) * 2 + (
                           self.red.breakdown + self.red.mat_return + self.red.cut + self.red.stand_up) * 0.5 + (self.red.near_fall_4 * 4) - self.red.stalling) / (seconds / 60.0)

        blue_napm = blue_apm - red_apm
        red_napm = red_apm - blue_apm

        blue_vs = blue_weighted_result + (blue_napm * blue_npf)
        red_vs = red_weighted_result + (red_napm * red_npf)

        return blue_points, red_points, blue_npf, red_npf, blue_apm, red_apm, blue_escape_rate, blue_ride_rate, red_escape_rate, red_ride_rate, blue_napm, red_napm, blue_vs, red_vs


    # adapted MoV for pinfalls
    def pins(self):
        mov = self.scores()[0] - self.scores()[1]
        result = self.result

        if result == 'WinF':
            mov = 25
        elif result == 'LossF':
            mov = 25
        return mov


    def ranking_fun(self, x):
        Ra1 = Wrestler.objects.get(name=self.blue.name)
        Rb1 = Wrestler.objects.get(name=self.red.name)

        Ra = Ra1.rating
        Rb = Rb1.rating

        # sets binary result
        if self.result == 'WinF':
            Sa = 1
        elif self.result == 'WinTF':
            Sa = 1
        elif self.result == 'WinMD':
            Sa = 1
        elif self.result == 'WinD':
            Sa = 1
        elif self.result == 'LossD':
            Sa = 0
        elif self.result == 'LossMD':
            Sa = 0
        elif self.result == 'LossTF':
            Sa = 0
        elif self.result == 'LossF':
            Sa = 0

        elo_dif = Ra - Rb

        Ea = 1 / (1 + 10 ** ((Rb - Ra) / 400))
        print('Blue chance to win:', round(Ea, 2), '\nResult:', Sa)

        potential = K * (Sa - Ea)

        factor = ((abs(self.pins()) + 3) ** 0.8) / (7.5 + (0.006 * elo_dif))
        change = factor * potential
        print('Change: ', abs(round(change, 0)))

        nRa = round(Ra + change, 0)
        print('New Blue Rating =', round(nRa, 0))
        Ra1.rating = int(nRa)
        Ra1.save()
        nRb = round(Rb - change, 0)
        print('New Red Rating =', round(nRb, 0))
        Rb1.rating = int(nRb)
        Rb1.save()
        return



    def close_fun(self):
        # prepping matchdata model

        data1 = [self.match_id, self.blue.name, self.red.name, self.blue.team, self.red.team, self.weight, datetime.datetime.today().strftime('%Y-%m-%d'), self.result, self.scores()[0], self.scores()[1], (self.scores()[0] - self.scores()[1]),
                seconds, self.blue.head_inside_attempt, self.blue.head_inside_conversion, self.blue.head_outside_attempt, self.blue.head_outside_conversion, self.blue.double_attempt, self.blue.double_conversion, self.blue.low_shot_attempt, self.blue.low_shot_conversion,
                self.blue.go_behind_attempt, self.blue.go_behind_conversion, self.blue.throw_attempt, self.blue.throw_conversion, self.blue.stand_up, self.blue.escape, self.blue.reversal, self.blue.cut, self.blue.breakdown, self.blue.mat_return, self.blue.near_fall_2, self.blue.near_fall_4, self.blue.caution,
                self.blue.stalling, self.blue.technical_violation, self.blue.riding_time, self.red.head_inside_attempt, self.red.head_inside_conversion, self.red.head_outside_attempt, self.red.head_outside_conversion, self.red.double_attempt, self.red.double_conversion,
                self.red.low_shot_attempt, self.red.low_shot_conversion,
                self.red.go_behind_attempt, self.red.go_behind_conversion, self.red.throw_attempt, self.red.throw_conversion, self.red.stand_up, self.red.escape, self.red.reversal, self.red.cut, self.red.breakdown, self.red.mat_return, self.red.near_fall_2, self.red.near_fall_4,
                self.red.caution, self.red.stalling, self.red.technical_violation, self.red.riding_time, self.blue.comp()[0], self.blue.comp()[1], self.blue.comp()[2], self.blue.comp()[3], self.blue.comp()[4], self.blue.comp()[5], self.blue.comp()[6], self.scores()[6],
                self.scores()[7], self.scores()[2], self.scores()[4], self.scores()[-2], self.red.comp()[0], self.red.comp()[1], self.red.comp()[2], self.red.comp()[3], self.red.comp()[4], self.red.comp()[5], self.red.comp()[6], self.scores()[8], self.scores()[9], self.scores()[3],
                self.scores()[5], self.scores()[-1]]

        data2 = [self.match_id + '_', self.red.name, self.blue.name, self.red.team, self.blue.team, self.weight, datetime.datetime.today().strftime('%Y-%m-%d'), self.opp_result, self.scores()[1], self.scores()[0], (self.scores()[1] - self.scores()[0]),
                seconds, self.red.head_inside_attempt, self.red.head_inside_conversion, self.red.head_outside_attempt, self.red.head_outside_conversion, self.red.double_attempt, self.red.double_conversion, self.red.low_shot_attempt, self.red.low_shot_conversion,
                self.red.go_behind_attempt, self.red.go_behind_conversion, self.red.throw_attempt, self.red.throw_conversion, self.red.stand_up, self.red.escape, self.red.reversal, self.red.cut, self.red.breakdown, self.red.mat_return, self.red.near_fall_2, self.red.near_fall_4, self.red.caution,
                self.red.stalling, self.red.technical_violation, self.red.riding_time, self.blue.head_inside_attempt, self.blue.head_inside_conversion, self.blue.head_outside_attempt, self.blue.head_outside_conversion, self.blue.double_attempt, self.blue.double_conversion,
                self.blue.low_shot_attempt, self.blue.low_shot_conversion,
                self.blue.go_behind_attempt, self.blue.go_behind_conversion, self.blue.throw_attempt, self.blue.throw_conversion, self.blue.stand_up, self.blue.escape, self.blue.reversal, self.blue.cut, self.blue.breakdown, self.blue.mat_return, self.blue.near_fall_2, self.blue.near_fall_4,
                self.blue.caution, self.blue.stalling, self.blue.technical_violation, self.blue.riding_time, self.red.comp()[0], self.red.comp()[1], self.red.comp()[2], self.red.comp()[3], self.red.comp()[4], self.red.comp()[5], self.red.comp()[6], self.scores()[8],
                self.scores()[9], self.scores()[3], self.scores()[5], self.scores()[-1], self.blue.comp()[0], self.blue.comp()[1], self.blue.comp()[2], self.blue.comp()[3], self.blue.comp()[4], self.blue.comp()[5], self.blue.comp()[6], self.scores()[6], self.scores()[7], self.scores()[2],
                self.scores()[4], self.scores()[-2]]

        match_obj = Matchdata.objects.filter(matchID=data1[0]).update(
            date = data1[6],
            focus = data1[1],
            focus_team = data1[3],
            opponent = data1[2],
            opp_team = data1[4],
            focus_score = data1[8],
            opp_score = data1[9],
            result = data1[7],
            weight = data1[5],
            mov = data1[10],
            duration = data1[11],
            hia = data1[12],
            hic = data1[13],
            hoa = data1[14],
            hoc = data1[15],
            da = data1[16],
            dc = data1[17],
            lsa = data1[18],
            lsc = data1[19],
            gba = data1[20],
            gbc = data1[21],
            ta = data1[22],
            tc = data1[22],
            su = data1[24],
            e = data1[25],
            r = data1[26],
            cut = data1[27],
            bd = data1[28],
            mr = data1[29],
            nf2 = data1[30],
            nf4 = data1[31],
            caution = data1[32],
            tv = data1[33],
            rt = data1[34],
            opp_hia = data1[35],
            opp_hic = data1[36],
            opp_hoa = data1[37],
            opp_hoc = data1[38],
            opp_da = data1[39],
            opp_dc = data1[40],
            opp_lsa = data1[41],
            opp_lsc = data1[42],
            opp_gba = data1[43],
            opp_gbc = data1[44],
            opp_ta = data1[45],
            opp_tc = data1[46],
            opp_su = data1[47],
            opp_e = data1[48],
            opp_r = data1[49],
            opp_cut = data1[50],
            opp_bd = data1[51],
            opp_mr = data1[52],
            opp_nf2 = data1[53],
            opp_nf4 = data1[54],
            opp_caution = data1[55],
            opp_tv = data1[56],
            opp_rt = data1[57],
            hi_rate = data1[58],
            ho_rate = data1[59],
            d_rate = data1[60],
            ls_rate = data1[61],
            gb_rate = data1[62],
            t_rate = data1[63],
            td_rate = data1[64],
            e_rate = data1[65],
            ride_rate = data1[66],
            apm = data1[66],
            vs = data1[67],
            opp_hi_rate = data1[68],
            opp_ho_rate = data1[69],
            opp_d_rate = data1[70],
            opp_ls_rate = data1[71],
            opp_gb_rate = data1[72],
            opp_t_rate = data1[73],
            opp_td_rate = data1[74],
            opp_e_rate = data1[75],
            opp_ride_rate = data1[76],
            opp_apm = data1[77],
            opp_vs = data1[78],
        )

        # to csv in collector directory
        rawcolumns = ['MatchID', 'Focus', 'Opponent', 'FocusTeam', 'OppTeam', 'Weight', 'Date', 'Result', 'FocusPoints', 'OppPoints', 'MoV', 'Time', 'HIa', 'HIc', 'HOa', 'HOc', 'Da', 'Dc', 'LSa', 'LSc', 'GBa', 'GBc', 'Ta',
                      'Tc', 'SU', 'E', 'R', 'Cut', 'BD', 'MR', 'NF2', 'NF4', 'Caution', 'S', 'TV', 'RT', 'oHIa', 'oHIc', 'oHOa', 'oHOc', 'oDa', 'oDc', 'oLSa', 'oLSc', 'oGBa', 'oGBc', 'oTa', 'oTc',
                      'oSU', 'oE', 'oR', 'oCut', 'oBD', 'oMR', 'oNF2', 'oNF4', 'oCaution', 'oS', 'oTV', 'oRT', 'HIrate', 'HOrate', 'Drate', 'LSrate', 'GBrate', 'Trate', 'TDrate', 'Erate', 'Riderate', 'NPF', 'APM', 'VS',
                      'oHIrate', 'oHOrate', 'oDrate', 'oLSrate', 'oGBrate', 'oTrate', 'oTDrate', 'oErate', 'oRiderate', 'oNPF', 'oAPM', 'oVS']

        matchdata = pd.DataFrame(columns=rawcolumns)
        matchdata = matchdata.append(pd.Series(data1, index=rawcolumns), ignore_index=True)
        matchdata = matchdata.append(pd.Series(data2, index=rawcolumns), ignore_index=True)
        matchdata = matchdata.set_index('MatchID')

        if not os.path.isfile('matchdata.csv'):
            matchdata.to_csv('matchdata.csv', mode='w', header=True)
        else:
            matchdata.to_csv('matchdata.csv', mode='a', header=False)

        if not os.path.isfile('match_timeseries.csv'):
            match_timeseries.to_csv('match_timeseries.csv', mode='w', header=True)
        else:
            match_timeseries.to_csv('match_timeseries.csv', mode='a', header=False)


# main call
Events()
