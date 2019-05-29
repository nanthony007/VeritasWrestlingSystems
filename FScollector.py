import tkinter as tk
from tkinter import messagebox
from tkinter import ttk as ttk
import pandas as pd
import time
import sys
import datetime
from pandastable import Table
from PIL import ImageTk, Image
import string
import random
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()
from vws_main.models import FS_Wrestler, FS_Match, FS_TS, FS_Team
from collection import backend
pd.options.mode.chained_assignment = None

# wrestlers = pd.read_csv("collection/stats/wrestlers.csv")
# wrestlers = wrestlers.set_index('Name')


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


# restarts program
def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)


class StopWatch(tk.Frame):
    """ Implements a stop watch frame widget. """

    def __init__(self, parent=None, **kw):
        tk.Frame.__init__(self, parent, kw)
        self._start = 0.0
        self._elapsedtime = 0.0
        self._running = 0
        self.timestr = tk.StringVar()
        self.makewidgets()

    def makewidgets(self):
        """ Make the time label. """
        self.timer = tk.Label(self, textvariable=self.timestr, font='Helvetica 15', fg='white', bg='slate gray', padx='25px', pady='10px')
        self._settime(self._elapsedtime)
        self.timer.pack(fill=tk.X, expand=tk.NO)

    def _update(self):
        """ Update the label with elapsed time. """
        self._elapsedtime = time.time() - self._start
        self._settime(self._elapsedtime)
        self._timer = self.after(50, self._update)

    def _settime(self, elap):
        """ Set the time string to Minutes:Seconds:Hundreths """
        minutes = int(elap / 60)
        seconds = int(elap - minutes * 60.0)
        hseconds = int((elap - minutes * 60.0 - seconds) * 100)
        self.timestr.set('%02d:%02d:%02d' % (minutes, seconds, hseconds))

    def start(self):
        """ Start the stopwatch, ignore if running. """
        if not self._running:
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = 1

    def stop(self):
        """ Stop the stopwatch, ignore if stopped. """
        if self._running:
            self.after_cancel(self._timer)
            self._elapsedtime = time.time() - self._start
            self._settime(self._elapsedtime)
            self._running = 0

    def reset(self):
        """ Reset the stopwatch. """
        self._start = time.time()
        self._elapsedtime = 0.0
        self._settime(self._elapsedtime)


class Collector(tk.Tk):
    """
    Main application.  Used to collect data for Veritas Wrestling Systems.
    """

    def __init__(self, *args, **kwargs):
        """
        Starts by calling StartPage.
        Then by calling MatchPage (main collection screen) followed by
        ConfirmationPage.
        """
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Veritas Analytics")
        self._geom = '1400+800+0+0'
        img = tk.PhotoImage(file='collection/logo.png')
        self.tk.call('wm', 'iconphoto', self._w, img)
        self.bind('<Escape>', self.toggle_geom)

        self.shared_data = {
            'weight_class': tk.IntVar(),
            'blue_name': tk.StringVar(),
            'red_name': tk.StringVar(),
            'blue_team': tk.StringVar(),
            'red_team': tk.StringVar(),
            'blue_score': tk.IntVar(),
            'red_score': tk.IntVar(),
            'result': tk.StringVar(),
        }

        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, MatchPage, ConfirmationPage):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        """
        Shows frame that is passed as argument.
        """
        frame = self.frames[cont]
        frame.tkraise()

    def get_page(self, page_class):
        """
        Gets data from page as argument.
        """
        return self.frames[page_class]

    def toggle_geom(self, event):
        """
        Toggles full-screen or windowed geometry.
        """
        geom = tk.Tk.winfo_geometry(self)
        tk.Tk.wm_geometry(self, self._geom)
        self._geom = geom


class StartPage(tk.Frame):
    """
    Initial page.
    User selects wrestlers and weight class.
    """

    def __init__(self, parent, controller):
        """
        Initializes frames for window and wrestler names based on dropdown.
        """
        tk.Frame.__init__(self, parent, bg='slate gray')
        self.controller = controller
        self.blue_frame = tk.LabelFrame(self, text='Blue Info', fg='blue', bg='slate gray')
        self.blue_frame.pack(side=tk.RIGHT, anchor=tk.NW, padx='50px', pady='50px')
        self.red_frame = tk.LabelFrame(self, text='Red Info', fg='red', bg='slate gray')
        self.red_frame.pack(side=tk.LEFT, anchor=tk.NE, padx='50px', pady='50px')

        image = Image.open("collection/logo.png")
        image = image.resize((400,300), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(self, image=photo)
        label.image = photo  # keep a reference!
        label.pack(side=tk.TOP)

        self.intro_text = tk.StringVar()
        self.intro_text.set("Welcome to the Veritas Wrestling Systems Data Collection Application! "
                            "\n\nTo begin, simply select the appropriate teams and the correpsonding athletes. "
                            "\n\nThen select the competition weight class and hit 'Start New Match' to begin.")
        self.intro = tk.Message(self, textvariable=self.intro_text, bg='slate gray', font='Helvetica 16')
        self.intro.config(anchor=tk.CENTER)
        self.intro.pack(side=tk.TOP, pady='20px')

        db_wrestlers = FS_Wrestler.objects.values_list(
            'name', 'team', 'rating').order_by('name')
        self.wrestler_list = []
        for i in db_wrestlers:
            self.wrestler_list.append(i[0])

        self.weight_class_dropdown = ttk.Combobox(self, state='readonly', values=[57, 61, 65, 70, 74, 79, 86, 92, 97, 125], font='Helvetica 12')
        self.weight_class_dropdown.set('Select Weight Class:')
        self.weight_class_dropdown.pack(side=tk.TOP, padx='50px', pady='20px')

        self.start_new_match_button = tk.Button(self, text="Start New Match", command=combine_funcs(self.start_match, lambda: controller.show_frame(MatchPage)), bg='slate gray', font='Helvetica 12')
        self.start_new_match_button.pack(side=tk.TOP, padx='50px', pady='20px')
        self.create_widgets()

    def blue_CurSelect(self, event):
        value = self.blue_lbox.get(self.blue_lbox.curselection())
        self.blue_search.set(value)
        print(self.blue_search.get())

    def red_CurSelect(self, event):
        value = self.red_lbox.get(self.red_lbox.curselection())
        self.red_search.set(value)
        print(self.search.get())

    def create_widgets(self):
        self.blue_search = tk.StringVar()
        self.blue_search.trace("w", lambda name, index, mode: self.update_list_blue())
        self.blue_entry = tk.Entry(self.blue_frame, textvariable=self.blue_search, font='Helvetica 16')
        self.blue_lbox = tk.Listbox(self.blue_frame, font='Helvetica 14')
        self.blue_lbox.bind('<<ListboxSelect>>', self.blue_CurSelect)
        self.blue_entry.pack(side=tk.TOP, fill=tk.BOTH, expand=1, padx='25px', pady='25px')
        self.blue_lbox.pack(side=tk.TOP, fill=tk.BOTH, expand=1, padx='25px', pady='25px')

        self.red_search = tk.StringVar()
        self.red_search.trace("w", lambda name, index, mode: self.update_list_red())
        self.red_entry = tk.Entry(self.red_frame, textvariable=self.red_search, font='Helvetica 16')
        self.red_lbox = tk.Listbox(self.red_frame, font='Helvetica 12')
        self.red_lbox.bind('<<ListboxSelect>>', self.red_CurSelect)
        self.red_entry.pack(side=tk.TOP, fill=tk.BOTH, expand=1, padx='25px', pady='25px')
        self.red_lbox.pack(side=tk.TOP, fill=tk.BOTH, expand=1, padx='25px', pady='25px')

        # Function for updating the list/doing the search.
        # It needs to be called here to populate the listbox.
        self.update_list_blue()
        self.update_list_red()

    def update_list_blue(self):
        search_term = self.blue_search.get()
        # Just a generic list to populate the listbox
        lbox_list = self.wrestler_list

        self.blue_lbox.delete(0, tk.END)

        for item in lbox_list:
            if search_term.lower() in item.lower():
                self.blue_lbox.insert(tk.END, item)

        self.blue_search.set(self.blue_search.get())

    def update_list_red(self):
        search_term = self.red_search.get()
        # Just a generic list to populate the listbox
        lbox_list =self.wrestler_list

        self.red_lbox.delete(0, tk.END)

        for item in lbox_list:
            if search_term.lower() in item.lower():
                self.red_lbox.insert(tk.END, item)

        self.red_search.set(self.red_search.get())


    def start_match(self):
        """
        Loads blue/red wrestlers from database.
        Opens MatchPage.
        """
        # intitializes wrestlers and global values
        blue = FS_Wrestler.objects.get(name=self.blue_search.get())
        red = FS_Wrestler.objects.get(name=self.red_search.get())

        bt1 = self.controller.shared_data['blue_name']
        bt1.set(blue.name)
        bt2 = self.controller.get_page(MatchPage)
        bt2.bluename.set(blue.name)

        bt3 = self.controller.shared_data['red_name']
        bt3.set(red.name)
        bt2.redname.set(red.name)

        bt5 = self.controller.shared_data['blue_team']
        bt5.set(blue.team.abbreviation)
        bt2.blueteam.set(blue.team.abbreviation)

        bt7 = self.controller.shared_data['red_team']
        bt7.set(red.team.abbreviation)
        bt2.redteam.set(red.team.abbreviation)

        bt2.blue_elo.set(blue.rating)
        bt2.red_elo.set(red.rating)

        bt11 = self.controller.shared_data['weight_class']
        bt11.set(self.weight_class_dropdown.get())
        bt2.weight_class_value.set(str(self.controller.shared_data['weight_class'].get()) + 'kgs')

        global m1
        m1 = FS_Match(matchID=bt2.matchID_value)
        m1.focus = blue
        m1.focus_team = m1.focus.team
        m1.opponent = red
        m1.opp_team = m1.opponent.team
        m1.save()
        global m2
        m2 = FS_Match(matchID=bt2.matchID_value + '*')
        m2.focus = red
        m2.focus_team = m2.focus.team
        m2.opponent = blue
        m2.opp_team = m2.opponent.team
        m2.save()


class MatchPage(tk.Frame):
    """
    Main page for data collection.
    Constitutes frames for each wrestler.
    Buttons inside frames append data to dataframes before upload to database.
    Real-time updates for timeseries.
    Table in center contains play-by-play for instant validation.
    Creates two match instances.
    Initializes two timeseries instances.
    # soon will include windowed video.
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # initializing primary frames
        self.blue_info = tk.LabelFrame(self, text='Blue Info:', fg='white', bg='blue')
        self.blue_info.grid(row=0, column=2, sticky=tk.NSEW)
        self.time_info = tk.Frame(self, bg='slate gray')
        self.time_info.grid(row=0, column=1, sticky=tk.NSEW)
        self.red_info = tk.LabelFrame(self, text='Red Info:', fg='white', bg='firebrick1')
        self.red_info.grid(row=0, column=0, sticky=tk.NSEW)
        self.play_by_play_frame = tk.LabelFrame(self, text='Play-by-Play:', fg='white', bg='slate gray')
        self.play_by_play_frame.grid(row=1, column=1, sticky=tk.NSEW)  # going to have timeseries table AND video view? --packed
        self.blue_buttons_frame = tk.LabelFrame(self, text='Blue Events:', fg='white', bg='blue')
        self.blue_buttons_frame.grid(row=1, column=2, sticky=tk.NSEW)
        self.blue_buttons_frame.grid_columnconfigure(0, weight=1)
        self.blue_buttons_frame.grid_columnconfigure(4, weight=1)
        self.blue_buttons_frame.grid_rowconfigure(0, weight=1)
        self.blue_buttons_frame.grid_rowconfigure(12, weight=1)
        self.red_buttons_frame = tk.LabelFrame(self, text='Red Events:', fg='white', bg='firebrick1')
        self.red_buttons_frame.grid(row=1, column=0, sticky=tk.NSEW)
        self.red_buttons_frame.grid_columnconfigure(0, weight=1)
        self.red_buttons_frame.grid_columnconfigure(4, weight=1)
        self.red_buttons_frame.grid_rowconfigure(0, weight=1)
        self.red_buttons_frame.grid_rowconfigure(12, weight=1)
        self.ending_frame = tk.LabelFrame(self, text='Results Info:', fg='white', bg='slate gray')
        self.ending_frame.grid(row=2, column=0, columnspan=3, sticky=tk.NSEW)
        self.match_info = tk.Frame(self.time_info, bg='slate gray')
        self.match_info.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        #self.blue_clock = tk.Frame(self.time_info, bg='slate gray')
        #self.blue_clock.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.clock_info = tk.Frame(self.time_info, bg='slate gray')
        self.clock_info.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        #self.red_clock = tk.Frame(self.time_info, bg='slate gray')
        #self.red_clock.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        # self.video_frame = tk.Frame(self.play_by_play_frame, bg='slate gray')
        # self.video_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.pbp_frame = tk.Frame(self.play_by_play_frame, bg='slate gray')
        self.pbp_frame.pack()

        # weighting for desired view
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=3)
        self.rowconfigure(2, weight=1)

        # initializing blue values
        self.blue_score = tk.IntVar()
        self.blue_score.set(0)
        self.blue_elo = tk.IntVar()
        self.bhia = 0
        self.bhic2 = 0
        self.bhic4 = 0
        self.bhoa = 0
        self.bhoc2 = 0
        self.bhoc4 = 0
        self.bda = 0
        self.bdc2 = 0
        self.bdc4 = 0
        self.blsa = 0
        self.blsc2 = 0
        self.blsc4 = 0
        self.bgba = 0
        self.bgbc = 0
        self.bta = 0
        self.btc2 = 0
        self.btc4 = 0
        self.bexposure = 0
        self.bgut = 0
        self.bleglace = 0
        self.bturn = 0
        self.brecovery = 0
        self.bpushout = 0
        self.bpassive = 0
        self.btv = 0
        self.bhi_rate = tk.DoubleVar()
        self.bho_rate = tk.DoubleVar()
        self.bd_rate = tk.DoubleVar()
        self.bls_rate = tk.DoubleVar()
        self.bgb_rate = tk.DoubleVar()
        self.bt_rate = tk.DoubleVar()
        self.b_result = tk.DoubleVar()
        self.result_abb = tk.StringVar()
        self.bweighted_result = tk.DoubleVar()
        self.b_npf = tk.DoubleVar()
        self.b_action = tk.DoubleVar()
        self.b_vs = tk.DoubleVar()

        # initializing red values
        self.red_score = tk.IntVar()
        self.red_score.set(0)
        self.red_elo = tk.IntVar()
        self.rhia = 0
        self.rhic2 = 0
        self.rhic4 = 0
        self.rhoa = 0
        self.rhoc2 = 0
        self.rhoc4 = 0
        self.rda = 0
        self.rdc2 = 0
        self.rdc4 = 0
        self.rlsa = 0
        self.rlsc2 = 0
        self.rlsc4 = 0
        self.rgba = 0
        self.rgbc = 0
        self.rta = 0
        self.rtc2 = 0
        self.rtc4 = 0
        self.rexposure = 0
        self.rgut = 0
        self.rleglace = 0
        self.rturn = 0
        self.rrecovery = 0
        self.rpushout = 0
        self.rpassive = 0
        self.rtv = 0
        self.rhi_rate = tk.DoubleVar()
        self.rho_rate = tk.DoubleVar()
        self.rd_rate = tk.DoubleVar()
        self.rls_rate = tk.DoubleVar()
        self.rgb_rate = tk.DoubleVar()
        self.rt_rate = tk.DoubleVar()
        self.r_result = tk.DoubleVar()
        self.result_opp_abb = tk.StringVar()
        self.rweighted_result = tk.DoubleVar()
        self.r_npf = tk.DoubleVar()
        self.r_action = tk.DoubleVar()
        self.r_vs = tk.DoubleVar()

        # info areas --grid
        self.blueteam = tk.StringVar()
        self.bluename = tk.StringVar()
        self.blue_wrestler_label = tk.Label(self.blue_info, textvariable=self.bluename, fg='white', bg='blue', bd=2, font='Helvetica 15 italic')
        self.blue_wrestler_label.pack(fill=tk.BOTH, expand=1)
        self.blue_team_label = tk.Label(self.blue_info, textvariable=self.blueteam, fg='white', bg='blue', bd=2, font='Helvetica 15')
        self.blue_team_label.pack(fill=tk.BOTH, expand=1)
        self.blue_rating_label = tk.Label(self.blue_info, textvariable=self.blue_elo, fg='white', bg='blue', bd=2, font='Helvetica 15 italic')
        self.blue_rating_label.pack(fill=tk.BOTH, expand=1)
        self.blue_points = tk.Label(self.blue_info, textvariable=self.blue_score, fg='white', bg='blue', bd=2, font='Helvetica 30 bold')
        self.blue_points.pack(fill=tk.BOTH, expand=1)

        self.redteam = tk.StringVar()
        self.redname = tk.StringVar()
        self.red_wrestler_label = tk.Label(self.red_info, textvariable=self.redname, fg='white', bg='firebrick1', bd=2, font='Helvetica 15 italic')
        self.red_wrestler_label.pack(fill=tk.BOTH, expand=1)
        self.red_team_label = tk.Label(self.red_info, textvariable=self.redteam, fg='white', bg='firebrick1', bd=2, font='Helvetica 15')
        self.red_team_label.pack(fill=tk.BOTH, expand=1)
        self.red_rating_label = tk.Label(self.red_info, textvariable=self.red_elo, fg='white', bg='firebrick1', bd=2, font='Helvetica 15 italic')
        self.red_rating_label.pack(fill=tk.BOTH, expand=1)
        self.red_points = tk.Label(self.red_info, textvariable=self.red_score, fg='white', bg='firebrick1', bd=2, font='Helvetica 30 bold')
        self.red_points.pack(fill=tk.BOTH, expand=1)

        # clock stuff --pack
        self.main_clock = StopWatch(self.clock_info)
        self.main_clock.timer.config(fg='white')
        self.main_clock.pack(side=tk.TOP, expand=1, pady=(0, 10))
        # self.blue_pass_clock = StopWatch(self.blue_clock)
        # self.blue_pass_clock.timer.config(fg='blue')
        # self.blue_pass_clock.pack(side=tk.LEFT, expand=1)
        # self.red_pass_clock = StopWatch(self.red_clock)
        # self.red_pass_clock.timer.config(fg='firebrick1')
        # self.red_pass_clock.pack(side=tk.RIGHT, expand=1)
        self.matchID_value = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
        self.matchID_label = tk.Label(self.match_info, text='MatchID: ' + self.matchID_value, font='Helvetica 12 italic', fg='white', bg='slate gray', padx='25px', pady='10px')
        self.matchID_label.pack(side=tk.LEFT, expand=1)
        self.weight_class_value = tk.IntVar()
        self.weight_class_label = tk.Label(self.match_info, textvariable=self.weight_class_value, font='Helvetica 12 italic', fg='white', bg='slate gray', padx='25px', pady='10px')
        self.weight_class_label.pack(side=tk.LEFT, expand=1)
        self.date_label = tk.Label(self.match_info, text='Date: ' + str(datetime.date.today()), font='Helvetica 12 italic', fg='white', bg='slate gray', padx='25px', pady='10px')
        self.date_label.pack(side=tk.LEFT, expand=1)
        self.start_button = tk.Button(self.clock_info, text='Start', command=self.main_clock.start, font='Helvetica 10', fg='white', bg='slate gray', padx='20px', pady='10px')
        self.start_button.pack(side=tk.LEFT, expand=1)
        self.stop_button = tk.Button(self.clock_info, text='Stop', command=self.main_clock.stop, font='Helvetica 10', fg='white', bg='slate gray', padx='20px', pady='10px')
        self.stop_button.pack(side=tk.RIGHT, expand=1)
        self.reset_button = tk.Button(self.clock_info, text='Reset', command=self.main_clock.reset, font='Helvetica 10', fg='white', bg='slate gray', padx='20px', pady='10px')
        self.reset_button.pack(side=tk.TOP, expand=1)

        # video area
        # put video in another window

        # timeseries table and df
        # change frame when add video
        self.event_lab = tk.IntVar()
        self.ts_df = pd.DataFrame(columns=['EventNum', 'EventLabel', 'EventTime', 'Blue', 'Red', 'matchID'])
        self.display_df = self.ts_df.drop(['Blue', 'Red', 'matchID'], axis=1)
        self.pbp = Table(parent=self.pbp_frame, dataframe=self.display_df, showstatusbar=True)
        self.pbp.grid(row=0, column=0)
        self.pbp.show()
        self.pbp.zoomIn()
        self.pbp.columncolors['EventNum'] = '#9999ff'
        self.pbp.columncolors['EventLabel'] = '#9999ff'
        self.pbp.columncolors['EventTime'] = '#9999ff'
        self.pbp.redraw()

        # blue buttons
        self.bhia_button = tk.Button(self.blue_buttons_frame, command=lambda: backend.bhia(self), text='Head Inside Attempt', font='Helvetica 8', relief='ridge', fg='white', bg='blue', bd=2).grid(row=1, column=1, sticky=tk.NSEW, padx='5px', pady='5px')
        self.bhic2_button = tk.Button(self.blue_buttons_frame, command=lambda: backend.bhic2(self), text='Head Inside Conversion(2)', font='Helvetica 8', relief='ridge', fg='white', bg='blue', bd=2).grid(row=1, column=2, sticky=tk.NSEW, padx='5px', pady='5px')
        self.bhic4_button = tk.Button(self.blue_buttons_frame, command=lambda: backend.bhic4(self), text='Head Inside Conversion(4)', font='Helvetica 8', relief='ridge', fg='white', bg='blue', bd=2).grid(row=1, column=3, sticky=tk.NSEW, padx='5px', pady='5px')
        self.bhoa_button = tk.Button(self.blue_buttons_frame, command=lambda: backend.bhoa(self), text='Head Outside Attempt', font='Helvetica 8', relief='ridge', fg='white', bg='blue', bd=2).grid(row=2, column=1, sticky=tk.NSEW, padx='5px', pady='5px')
        self.bhoc2_button = tk.Button(self.blue_buttons_frame, command=lambda: backend.bhoc2(self), text='Head Outside Conversion(2)', font='Helvetica 8', relief='ridge', fg='white', bg='blue', bd=2).grid(row=2, column=2, sticky=tk.NSEW, padx='5px', pady='5px')
        self.bhoc4_button = tk.Button(self.blue_buttons_frame, command=lambda: backend.bhoc4(self), text='Head Outside Conversion(4)', font='Helvetica 8', relief='ridge', fg='white', bg='blue', bd=2).grid(row=2, column=3, sticky=tk.NSEW, padx='5px', pady='5px')
        self.bda_button = tk.Button(self.blue_buttons_frame, command=lambda: backend.bda(self), text='Double Attempt', font='Helvetica 8', relief='ridge', fg='white', bg='blue', bd=2).grid(row=3, column=1, sticky=tk.NSEW, padx='5px', pady='5px')
        self.bdc2_button = tk.Button(self.blue_buttons_frame, command=lambda: backend.bdc2(self), text='Double Conversion(2)', font='Helvetica 8', relief='ridge', fg='white', bg='blue', bd=2).grid(row=3, column=2, sticky=tk.NSEW, padx='5px', pady='5px')
        self.bdc4_button = tk.Button(self.blue_buttons_frame, command=lambda: backend.bdc4(self), text='Double Conversion(4)', font='Helvetica 8', relief='ridge', fg='white', bg='blue', bd=2).grid(row=3, column=3, sticky=tk.NSEW, padx='5px', pady='5px')
        self.blsa_button = tk.Button(self.blue_buttons_frame, command=lambda: backend.blsa(self), text='LowShot Attempt', font='Helvetica 8', relief='ridge', fg='white', bg='blue', bd=2).grid(row=4, column=1, sticky=tk.NSEW, padx='5px', pady='5px')
        self.blsc2_button = tk.Button(self.blue_buttons_frame, command=lambda: backend.blsc2(self), text='LowShot Conversion(2)', font='Helvetica 8', relief='ridge', fg='white', bg='blue', bd=2).grid(row=4, column=2, sticky=tk.NSEW, padx='5px', pady='5px')
        self.blsc4_button = tk.Button(self.blue_buttons_frame, command=lambda: backend.blsc4(self), text='LowShot Conversion(4)', font='Helvetica 8', relief='ridge', fg='white', bg='blue', bd=2).grid(row=4, column=3, sticky=tk.NSEW, padx='5px', pady='5px')
        self.bgba_button = tk.Button(self.blue_buttons_frame, command=lambda: backend.bgba(self), text='GoBehind Attempt', font='Helvetica 8', relief='ridge', fg='white', bg='blue', bd=2).grid(row=5, column=1, sticky=tk.NSEW, padx='5px', pady='5px')
        self.bgbc_button = tk.Button(self.blue_buttons_frame, command=lambda: backend.bgbc(self), text='GoBehind Conversion', font='Helvetica 8', relief='ridge', fg='white', bg='blue', bd=2).grid(row=5, column=2, sticky=tk.NSEW, padx='5px', pady='5px')
        self.bta_button = tk.Button(self.blue_buttons_frame, command=lambda: backend.bta(self), text='Throw Attempt', font='Helvetica 8', relief='ridge', fg='white', bg='blue', bd=2).grid(row=6, column=1, sticky=tk.NSEW, padx='5px', pady='5px')
        self.btc2_button = tk.Button(self.blue_buttons_frame, command=lambda: backend.btc2(self), text='Throw Conversion(2)', font='Helvetica 8', relief='ridge', fg='white', bg='blue', bd=2).grid(row=6, column=2, sticky=tk.NSEW, padx='5px', pady='5px')
        self.btc4_button = tk.Button(self.blue_buttons_frame, command=lambda: backend.btc4(self), text='Throw Conversion(4)', font='Helvetica 8', relief='ridge', fg='white', bg='blue', bd=2).grid(row=6, column=3, sticky=tk.NSEW, padx='5px', pady='5px')
        self.bexposure_button = tk.Button(self.blue_buttons_frame, command=lambda: backend.bexposure(self), text='Exposure', font='Helvetica 8', relief='ridge', fg='white', bg='blue', bd=2).grid(row=7, column=1, columnspan=3, sticky=tk.NSEW, padx='5px', pady='5px')
        self.bleglace_button = tk.Button(self.blue_buttons_frame, command=lambda: backend.bleglace(self), text='Leg Lace', font='Helvetica 8', relief='ridge', fg='white', bg='blue', bd=2).grid(row=8, column=1, sticky=tk.NSEW, padx='5px', pady='5px')
        self.bgut_button = tk.Button(self.blue_buttons_frame, command=lambda: backend.bgut(self), text='Gut', font='Helvetica 8', relief='ridge', fg='white', bg='blue', bd=2).grid(row=8, column=2, sticky=tk.NSEW, padx='5px', pady='5px')
        self.bturn_button = tk.Button(self.blue_buttons_frame, command=lambda: backend.bturn(self), text='Turn', font='Helvetica 8', relief='ridge', fg='white', bg='blue', bd=2).grid(row=8, column=3, sticky=tk.NSEW, padx='5px', pady='5px')
        self.brecovery_button = tk.Button(self.blue_buttons_frame, command=lambda: backend.brecovery(self), text='Recovery', font='Helvetica 8', relief='ridge', fg='white', bg='blue', bd=2).grid(row=9, column=1, sticky=tk.NSEW, padx='5px', pady='5px')
        self.bpushout_button = tk.Button(self.blue_buttons_frame, command=lambda: backend.bpushout(self), text='Pushout', font='Helvetica 8', relief='ridge', fg='white', bg='blue', bd=2).grid(row=9, column=2, sticky=tk.NSEW, padx='5px', pady='5px')
        self.bpassive_button = tk.Button(self.blue_buttons_frame, command=lambda: backend.bpassive(self), text='Passive', font='Helvetica 8', relief='ridge', fg='white', bg='blue', bd=2).grid(row=10, column=1, sticky=tk.NSEW, padx='5px', pady='5px')
        self.btv1_button = tk.Button(self.blue_buttons_frame, command=lambda: backend.btv1(self), text='Violation(1)', font='Helvetica 8', relief='ridge', fg='white', bg='blue', bd=2).grid(row=10, column=2, sticky=tk.NSEW, padx='5px', pady='5px')
        self.btv2_button = tk.Button(self.blue_buttons_frame, command=lambda: backend.btv2(self), text='Violation(2)', font='Helvetica 8', relief='ridge', fg='white', bg='blue', bd=2).grid(row=10, column=3, sticky=tk.NSEW, padx='5px', pady='5px')

        # red buttons
        self.rhia_button = tk.Button(self.red_buttons_frame, command=lambda: backend.rhia(self), text='Head Inside Attempt', font='Helvetica 8', relief='ridge', fg='white', bg='red', bd=2).grid(row=1, column=1, sticky=tk.NSEW, padx='5px', pady='5px')
        self.rhic2_button = tk.Button(self.red_buttons_frame, command=lambda: backend.rhic2(self), text='Head Inside Conversion(2)', font='Helvetica 8', relief='ridge', fg='white', bg='red', bd=2).grid(row=1, column=2, sticky=tk.NSEW, padx='5px', pady='5px')
        self.rhic4_button = tk.Button(self.red_buttons_frame, command=lambda: backend.rhic4(self), text='Head Inside Conversion(4)', font='Helvetica 8', relief='ridge', fg='white', bg='red', bd=2).grid(row=1, column=3, sticky=tk.NSEW, padx='5px', pady='5px')
        self.rhoa_button = tk.Button(self.red_buttons_frame, command=lambda: backend.rhoa(self), text='Head Outside Attempt', font='Helvetica 8', relief='ridge', fg='white', bg='red', bd=2).grid(row=2, column=1, sticky=tk.NSEW, padx='5px', pady='5px')
        self.rhoc2_button = tk.Button(self.red_buttons_frame, command=lambda: backend.rhoc2(self), text='Head Outside Conversion(2)', font='Helvetica 8', relief='ridge', fg='white', bg='red', bd=2).grid(row=2, column=2, sticky=tk.NSEW, padx='5px', pady='5px')
        self.rhoc4_button = tk.Button(self.red_buttons_frame, command=lambda: backend.rhoc4(self), text='Head Outside Conversion(4)', font='Helvetica 8', relief='ridge', fg='white', bg='red', bd=2).grid(row=2, column=3, sticky=tk.NSEW, padx='5px', pady='5px')
        self.rda_button = tk.Button(self.red_buttons_frame, command=lambda: backend.rda(self), text='Double Attempt', font='Helvetica 8', relief='ridge', fg='white', bg='red', bd=2).grid(row=3, column=1, sticky=tk.NSEW, padx='5px', pady='5px')
        self.rdc2_button = tk.Button(self.red_buttons_frame, command=lambda: backend.rdc2(self), text='Double Conversion(2)', font='Helvetica 8', relief='ridge', fg='white', bg='red', bd=2).grid(row=3, column=2, sticky=tk.NSEW, padx='5px', pady='5px')
        self.rdc4_button = tk.Button(self.red_buttons_frame, command=lambda: backend.rdc4(self), text='Double Conversion(4)', font='Helvetica 8', relief='ridge', fg='white', bg='red', bd=2).grid(row=3, column=3, sticky=tk.NSEW, padx='5px', pady='5px')
        self.rlsa_button = tk.Button(self.red_buttons_frame, command=lambda: backend.rlsa(self), text='LowShot Attempt', font='Helvetica 8', relief='ridge', fg='white', bg='red', bd=2).grid(row=4, column=1, sticky=tk.NSEW, padx='5px', pady='5px')
        self.rlsc2_button = tk.Button(self.red_buttons_frame, command=lambda: backend.rlsc2(self), text='LowShot Conversion(2)', font='Helvetica 8', relief='ridge', fg='white', bg='red', bd=2).grid(row=4, column=2, sticky=tk.NSEW, padx='5px', pady='5px')
        self.rlsc4_button = tk.Button(self.red_buttons_frame, command=lambda: backend.rlsc4(self), text='LowShot Conversion(4)', font='Helvetica 8', relief='ridge', fg='white', bg='red', bd=2).grid(row=4, column=3, sticky=tk.NSEW, padx='5px', pady='5px')
        self.rgba_button = tk.Button(self.red_buttons_frame, command=lambda: backend.rgba(self), text='GoBehind Attempt', font='Helvetica 8', relief='ridge', fg='white', bg='red', bd=2).grid(row=5, column=1, sticky=tk.NSEW, padx='5px', pady='5px')
        self.rgbc_button = tk.Button(self.red_buttons_frame, command=lambda: backend.rgbc(self), text='GoBehind Conversion', font='Helvetica 8', relief='ridge', fg='white', bg='red', bd=2).grid(row=5, column=2, sticky=tk.NSEW, padx='5px', pady='5px')
        self.rta_button = tk.Button(self.red_buttons_frame, command=lambda: backend.rta(self), text='Throw Attempt', font='Helvetica 8', relief='ridge', fg='white', bg='red', bd=2).grid(row=6, column=1, sticky=tk.NSEW, padx='5px', pady='5px')
        self.rtc2_button = tk.Button(self.red_buttons_frame, command=lambda: backend.rtc2(self), text='Throw Conversion(2)', font='Helvetica 8', relief='ridge', fg='white', bg='red', bd=2).grid(row=6, column=2, sticky=tk.NSEW, padx='5px', pady='5px')
        self.rtc4_button = tk.Button(self.red_buttons_frame, command=lambda: backend.rtc4(self), text='Throw Conversion(4)', font='Helvetica 8', relief='ridge', fg='white', bg='red', bd=2).grid(row=6, column=3, sticky=tk.NSEW, padx='5px', pady='5px')
        self.rexposure_button = tk.Button(self.red_buttons_frame, command=lambda: backend.rexposure(self), text='Exposure', font='Helvetica 8', relief='ridge', fg='white', bg='red', bd=2).grid(row=7, column=1, columnspan=3, sticky=tk.NSEW, padx='5px', pady='5px')
        self.rleglace_button = tk.Button(self.red_buttons_frame, command=lambda: backend.rleglace(self), text='Leg Lace', font='Helvetica 8', relief='ridge', fg='white', bg='red', bd=2).grid(row=8, column=1, sticky=tk.NSEW, padx='5px', pady='5px')
        self.rgut_button = tk.Button(self.red_buttons_frame, command=lambda: backend.rgut(self), text='Gut', font='Helvetica 8', relief='ridge', fg='white', bg='red', bd=2).grid(row=8, column=2, sticky=tk.NSEW, padx='5px', pady='5px')
        self.rturn_button = tk.Button(self.red_buttons_frame, command=lambda: backend.rturn(self), text='Turn', font='Helvetica 8', relief='ridge', fg='white', bg='red', bd=2).grid(row=8, column=3, sticky=tk.NSEW, padx='5px', pady='5px')
        self.rrecovery_button = tk.Button(self.red_buttons_frame, command=lambda: backend.rrecovery(self), text='Recovery', font='Helvetica 8', relief='ridge', fg='white', bg='red', bd=2).grid(row=9, column=1, sticky=tk.NSEW, padx='5px', pady='5px')
        self.rpushout_button = tk.Button(self.red_buttons_frame, command=lambda: backend.rpushout(self), text='Pushout', font='Helvetica 8', relief='ridge', fg='white', bg='red', bd=2).grid(row=9, column=2, sticky=tk.NSEW, padx='5px', pady='5px')
        self.rpassive_button = tk.Button(self.red_buttons_frame, command=lambda: backend.rpassive(self), text='Passive', font='Helvetica 8', relief='ridge', fg='white', bg='red', bd=2).grid(row=10, column=1, sticky=tk.NSEW, padx='5px', pady='5px')
        self.rtv1_button = tk.Button(self.red_buttons_frame, command=lambda: backend.rtv1(self), text='Violation(1)', font='Helvetica 8', relief='ridge', fg='white', bg='red', bd=2).grid(row=10, column=2, sticky=tk.NSEW, padx='5px', pady='5px')
        self.rtv2_button = tk.Button(self.red_buttons_frame, command=lambda: backend.rtv2(self), text='Violation(2)', font='Helvetica 8', relief='ridge', fg='white', bg='red', bd=2).grid(row=10, column=3, sticky=tk.NSEW, padx='5px', pady='5px')

        # end of match detail frame
        self.result_values = ['Red Fall', 'Red Technical Fall', 'Red Decision', 'Blue Decision', 'Blue Technical Fall', 'Blue Fall']
        self.result_label = tk.Label(self.ending_frame, text='Select Result:', font='Helvetica 15 italic', fg='white', bg='slate gray', padx='25px', pady='10px')
        self.result_label.grid(row=0, column=0)
        self.result = ttk.Combobox(self.ending_frame, state='readonly', values=self.result_values, font='Helvetica 12')
        self.result.set('Select:')
        self.result.grid(row=0, column=1, padx='25px', pady='10px')
        self.upload_label = tk.Label(self.ending_frame, text='Finish match and upload.', font='Helvetica 15 italic', fg='white', bg='slate gray', padx='25px', pady='10px')
        self.upload_label.grid(row=0, column=3)
        self.warning_label = tk.Label(self.ending_frame, text='Be sure you have stopped recording', font='Helvetica 8', fg='white', bg='slate gray', padx='10px')
        self.warning_label.grid(row=1, column=3)
        self.upload_button = tk.Button(self.ending_frame, command=combine_funcs(self.proceed, lambda: controller.show_frame(ConfirmationPage)), text='Finalize', font='Helvetica 12', fg='white', bg='slate gray', padx='25px', pady='10px')
        self.upload_button.grid(row=0, column=4)

    def proceed(self):
        if self.result.get() == 'Select:':
            messagebox.showinfo(title="Info", message="You forgot to record the result!")

        self.controller.shared_data['result'].set(self.result.get())
        backend.num_result(self)  # calculates numeric result for use in below composite scores, provides string version of result for display in tables

        self.total_tda = self.bhia + self.bhoa + self.bda + self.blsa + self.bta + self.rhia + self.rhoa + self.rda + self.rlsa + self.rta
        self.total_tdc = self.bhic2 + self.bhoc2 + self.bdc2 + self.blsc2 + self.bgbc + self.btc2 + self.rhic2 + self.rhoc2 + self.rdc2 + self.rlsc2 + self.rgbc + self.rtc2 + \
                         self.bhic4 + self.bhoc4 + self.bdc4 + self.blsc4 + self.btc4 + self.rhic4 + self.rhoc4 + self.rdc4 + \
                         self.rlsc4 + self.rtc4

        # blue composite scores
        self.bhi_rate.set(round(safe_div(self.bhic2 + self.bhic4, self.bhia) * 100, 2))
        self.bho_rate.set(round(safe_div(self.bhoc2 + self.bhoc4, self.bhoa) * 100, 2))
        self.bd_rate.set(round(safe_div(self.bdc2 + self.bdc4, self.bda) * 100, 2))
        self.bls_rate.set(round(safe_div(self.blsc2 + self.blsc4, self.blsa) * 100, 2))
        self.bgb_rate.set(round(safe_div(self.bgbc, self.bgba) * 100, 2))
        self.bt_rate.set(round(safe_div(self.btc2 + self.btc4, self.bta) * 100, 2))
        self.bweighted_result.set(round(self.b_result.get() * (FS_Wrestler.objects.get(name=self.controller.shared_data['red_name'].get()).rating / 100), 2))
        self.b_npf.set(round(safe_div((self.bhia + self.bhoa + self.bda + self.blsa + self.bta), self.total_tda) +
                             safe_div((self.bhic2 + self.bhoc2 + self.bdc2 + self.blsc2 + self.bgbc + self.btc2 + self.bhic4 + self.bhoc4 + self.bdc4 + self.blsc4 + self.btc4), self.total_tdc), 2))
        self.b_action.set(round(self.bhia + self.bhoa + self.bda + self.blsa + self.bgba + self.bta + self.bpushout + self.brecovery +
                                (self.bhic2 + self.bhoc2 + self.bdc2 + self.blsc2 + self.bgbc + self.btc2 + + self.bexposure + self.bturn + self.bleglace + self.bgut) * 2 +
                                (self.bhic4 + self.bhoc4 + self.bdc4 + self.blsc4 + self.btc4) * 4 - self.bpassive - self.btv, 2))
        self.b_vs.set(round(self.bweighted_result.get() + (self.b_action.get() - self.r_action.get()) * self.b_npf.get(), 2))

        # red composite scores
        self.rhi_rate.set(round(safe_div(self.rhic2 + self.rhic4, self.rhia) * 100, 2))
        self.rho_rate.set(round(safe_div(self.rhoc2 + self.rhoc4, self.rhoa) * 100, 2))
        self.rd_rate.set(round(safe_div(self.rdc2 + self.rdc4, self.rda) * 100, 2))
        self.rls_rate.set(round(safe_div(self.rlsc2 + self.rlsc4, self.rlsa) * 100, 2))
        self.rgb_rate.set(round(safe_div(self.rgbc, self.rgba) * 100, 2))
        self.rt_rate.set(round(safe_div(self.rtc2 + self.rtc4, self.rta) * 100, 2))
        self.rweighted_result.set(round(self.r_result.get() * (FS_Wrestler.objects.get(name=self.controller.shared_data['blue_name'].get()).rating / 100), 2))
        self.r_npf.set(round(safe_div((self.rhia + self.rhoa + self.rda + self.rlsa + self.rta), self.total_tda) +
                             safe_div((self.rhic2 + self.rhoc2 + self.rdc2 + self.rlsc2 + self.rgbc + self.rtc2 + self.rhic4 + self.rhoc4 + self.rdc4 + self.rlsc4 + self.rtc4), self.total_tdc), 2))
        self.r_action.set(round(self.rhia + self.rhoa + self.rda + self.rlsa + self.rgba + self.rta + self.rpushout + self.rrecovery +
                                (self.rhic2 + self.rhoc2 + self.rdc2 + self.rlsc2 + self.rgbc + self.rtc2 + + self.rexposure + self.rturn + self.rleglace + self.rgut) * 2 +
                                (self.rhic4 + self.rhoc4 + self.rdc4 + self.rlsc4 + self.rtc4) * 4 - self.rpassive - self.rtv, 2))
        self.r_vs.set(round(self.rweighted_result.get() + (self.r_action.get() - self.b_action.get()) * self.r_npf.get(), 2))


class ConfirmationPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config(bg='slate gray')

        x = self.controller.get_page(MatchPage)  # needed to get MatchPage values

        # five frames for window
        self.above_frame = tk.LabelFrame(self, text='Navigate:', fg='white', bg='slate gray')
        self.blue_comp_frame = tk.LabelFrame(self, text='Blue Stats:', fg='white', bg='slate gray')
        self.text_frame = tk.LabelFrame(self, text='Rating Changes:', fg='white', bg='slate gray')
        self.red_comp_frame = tk.LabelFrame(self, text='Red Stats:', fg='white', bg='slate gray')
        self.below_frame = tk.LabelFrame(self, text='Restart:', fg='white', bg='slate gray')
        self.above_frame.grid(row=0, column=1, sticky=tk.NSEW)
        self.blue_comp_frame.grid(row=1, column=2, sticky=tk.NSEW)
        self.text_frame.grid(row=1, column=1, sticky=tk.NSEW)
        self.red_comp_frame.grid(row=1, column=0, sticky=tk.NSEW)
        self.below_frame.grid(row=2, column=1, sticky=tk.NSEW)

        # formatting
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=3)
        self.rowconfigure(2, weight=1)

        self.blue_comp_frame.columnconfigure(0, weight=1)
        self.blue_comp_frame.columnconfigure(1, weight=1)
        self.red_comp_frame.columnconfigure(0, weight=1)
        self.red_comp_frame.columnconfigure(1, weight=1)

        # blue comp labels
        self.bhi_rate_label = tk.Label(self.blue_comp_frame, textvariable=x.bhi_rate, bg='slate gray', fg='white', font='Helvetica 15').grid(row=0, column=1, sticky=tk.NSEW)
        self.bho_rate_label = tk.Label(self.blue_comp_frame, textvariable=x.bho_rate, bg='slate gray', fg='white', font='Helvetica 15').grid(row=1, column=1, sticky=tk.NSEW)
        self.bd_rate_label = tk.Label(self.blue_comp_frame, textvariable=x.bd_rate, bg='slate gray', fg='white', font='Helvetica 15').grid(row=2, column=1, sticky=tk.NSEW)
        self.bls_rate_label = tk.Label(self.blue_comp_frame, textvariable=x.bls_rate, bg='slate gray', fg='white', font='Helvetica 15').grid(row=3, column=1, sticky=tk.NSEW)
        self.bgb_rate_label = tk.Label(self.blue_comp_frame, textvariable=x.bgb_rate, bg='slate gray', fg='white', font='Helvetica 15').grid(row=4, column=1, sticky=tk.NSEW)
        self.bt_rate_label = tk.Label(self.blue_comp_frame, textvariable=x.bt_rate, bg='slate gray', fg='white', font='Helvetica 15').grid(row=5, column=1, sticky=tk.NSEW)
        self.b_apm_label = tk.Label(self.blue_comp_frame, textvariable=x.b_action, bg='slate gray', fg='white', font='Helvetica 15').grid(row=6, column=1, sticky=tk.NSEW)
        self.b_npf_label = tk.Label(self.blue_comp_frame, textvariable=x.b_npf, bg='slate gray', fg='white', font='Helvetica 15').grid(row=7, column=1, sticky=tk.NSEW)
        self.b_vs_label = tk.Label(self.blue_comp_frame, textvariable=x.b_vs, bg='slate gray', fg='white', font='Helvetica 15').grid(row=8, column=1, sticky=tk.NSEW)
        self.bweighted_result_label = tk.Label(self.blue_comp_frame, textvariable=x.bweighted_result, bg='slate gray', fg='white', font='Helvetica 15').grid(row=9, column=1, sticky=tk.NSEW)

        self.blue_hirate = tk.Label(self.blue_comp_frame, text='Blue HI%:', bg='slate gray', fg='white', font='Helvetica 15').grid(row=0, column=0, sticky=tk.NSEW)
        self.blue_horate = tk.Label(self.blue_comp_frame, text='Blue HO%:', bg='slate gray', fg='white', font='Helvetica 15').grid(row=1, column=0, sticky=tk.NSEW)
        self.blue_drate = tk.Label(self.blue_comp_frame, text='Blue Double%:', bg='slate gray', fg='white', font='Helvetica 15').grid(row=2, column=0, sticky=tk.NSEW)
        self.blue_lsrate = tk.Label(self.blue_comp_frame, text='Blue LowShot%:', bg='slate gray', fg='white', font='Helvetica 15').grid(row=3, column=0, sticky=tk.NSEW)
        self.blue_gbrate = tk.Label(self.blue_comp_frame, text='Blue Counter%:', bg='slate gray', fg='white', font='Helvetica 15').grid(row=4, column=0, sticky=tk.NSEW)
        self.blue_trate = tk.Label(self.blue_comp_frame, text='Blue Throw%:', bg='slate gray', fg='white', font='Helvetica 15').grid(row=5, column=0, sticky=tk.NSEW)
        self.blue_apm = tk.Label(self.blue_comp_frame, text='Blue APM:', bg='slate gray', fg='white', font='Helvetica 15').grid(row=6, column=0, sticky=tk.NSEW)
        self.blue_npf = tk.Label(self.blue_comp_frame, text='Blue NPF:', bg='slate gray', fg='white', font='Helvetica 15').grid(row=7, column=0, sticky=tk.NSEW)
        self.blue_vs = tk.Label(self.blue_comp_frame, text='Blue Veritas Score:', bg='slate gray', fg='white', font='Helvetica 15').grid(row=8, column=0, sticky=tk.NSEW)
        self.blue_WR = tk.Label(self.blue_comp_frame, text='Blue Weighted Result:', bg='slate gray', fg='white', font='Helvetica 15').grid(row=9, column=0, sticky=tk.NSEW)

        # red comp labels
        self.rhi_rate_label = tk.Label(self.red_comp_frame, textvariable=x.rhi_rate, bg='slate gray', fg='white', font='Helvetica 15').grid(row=0, column=1, sticky=tk.NSEW)
        self.rho_rate_label = tk.Label(self.red_comp_frame, textvariable=x.rho_rate, bg='slate gray', fg='white', font='Helvetica 15').grid(row=1, column=1, sticky=tk.NSEW)
        self.rd_rate_label = tk.Label(self.red_comp_frame, textvariable=x.rd_rate, bg='slate gray', fg='white', font='Helvetica 15').grid(row=2, column=1, sticky=tk.NSEW)
        self.rls_rate_label = tk.Label(self.red_comp_frame, textvariable=x.rls_rate, bg='slate gray', fg='white', font='Helvetica 15').grid(row=3, column=1, sticky=tk.NSEW)
        self.rgb_rate_label = tk.Label(self.red_comp_frame, textvariable=x.rgb_rate, bg='slate gray', fg='white', font='Helvetica 15').grid(row=4, column=1, sticky=tk.NSEW)
        self.rt_rate_label = tk.Label(self.red_comp_frame, textvariable=x.rt_rate, bg='slate gray', fg='white', font='Helvetica 15').grid(row=5, column=1, sticky=tk.NSEW)
        self.r_apm_label = tk.Label(self.red_comp_frame, textvariable=x.r_action, bg='slate gray', fg='white', font='Helvetica 15').grid(row=6, column=1, sticky=tk.NSEW)
        self.r_npf_label = tk.Label(self.red_comp_frame, textvariable=x.r_npf, bg='slate gray', fg='white', font='Helvetica 15').grid(row=7, column=1, sticky=tk.NSEW)
        self.r_vs_label = tk.Label(self.red_comp_frame, textvariable=x.r_vs, bg='slate gray', fg='white', font='Helvetica 15').grid(row=8, column=1, sticky=tk.NSEW)
        self.rweighted_result_label = tk.Label(self.red_comp_frame, textvariable=x.rweighted_result, bg='slate gray', fg='white', font='Helvetica 15').grid(row=9, column=1, sticky=tk.NSEW)

        self.red_hirate = tk.Label(self.red_comp_frame, text='Red HI%:', bg='slate gray', fg='white', font='Helvetica 15').grid(row=0, column=0, sticky=tk.NSEW)
        self.red_horate = tk.Label(self.red_comp_frame, text='Red HO%:', bg='slate gray', fg='white', font='Helvetica 15').grid(row=1, column=0, sticky=tk.NSEW)
        self.red_drate = tk.Label(self.red_comp_frame, text='Red Double%:', bg='slate gray', fg='white', font='Helvetica 15').grid(row=2, column=0, sticky=tk.NSEW)
        self.red_lsrate = tk.Label(self.red_comp_frame, text='Red LowShot%:', bg='slate gray', fg='white', font='Helvetica 15').grid(row=3, column=0, sticky=tk.NSEW)
        self.red_gbrate = tk.Label(self.red_comp_frame, text='Red Counter%:', bg='slate gray', fg='white', font='Helvetica 15').grid(row=4, column=0, sticky=tk.NSEW)
        self.red_trate = tk.Label(self.red_comp_frame, text='Red Throw%:', bg='slate gray', fg='white', font='Helvetica 15').grid(row=5, column=0, sticky=tk.NSEW)
        self.red_apm = tk.Label(self.red_comp_frame, text='Red APM:', bg='slate gray', fg='white', font='Helvetica 15').grid(row=6, column=0, sticky=tk.NSEW)
        self.red_npf = tk.Label(self.red_comp_frame, text='Red NPF:', bg='slate gray', fg='white', font='Helvetica 15').grid(row=7, column=0, sticky=tk.NSEW)
        self.red_vs = tk.Label(self.red_comp_frame, text='Red Veritas Score:', bg='slate gray', fg='white', font='Helvetica 15').grid(row=8, column=0, sticky=tk.NSEW)
        self.red_WR = tk.Label(self.red_comp_frame, text='Red Weighted Result:', bg='slate gray', fg='white', font='Helvetica 15').grid(row=9, column=0, sticky=tk.NSEW)

        # nav buttons
        self.back_button = tk.Button(self.above_frame, text='Back', command=lambda: controller.show_frame(MatchPage), fg='white', bg='slate gray', font='Helvetica 20')
        self.back_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.upload_button = tk.Button(self.above_frame, text='Upload', command=self.upload, fg='white', bg='slate gray', font='Helvetica 20')
        self.upload_button.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

        self.restart_button = tk.Button(self.below_frame, text="Start a New Match", command=restart_program, fg='white', bg='slate gray', font='Helvetica 20')
        self.restart_button.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

        self.textbox = tk.Text(self.text_frame, background='slate gray', foreground='white', relief=tk.SUNKEN, font='Helvetica 12')
        self.textbox.tag_config('center-tag', justify=tk.CENTER)
        self.textbox.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.textbox.config(state=tk.NORMAL)
        self.textbox.insert(tk.END, '\n---------\n', 'center-tag')
        self.textbox.insert(tk.END,
            'The upload process may take a few moments', 'center-tag')

    def upload(self):
        self.x = self.controller.get_page(MatchPage)

        # matchdata stuff
        rawcolumns = ['MatchID', 'Focus', 'Opponent', 'FocusTeam', 'OppTeam', 'Weight', 'Date', 'Result', 'FocusPoints', 'OppPoints', 'MoV', 'Time',
                      'HIa', 'HIc2', 'HIc4', 'HOa', 'HOc2', 'HOc4', 'Da', 'Dc2', 'Dc4', 'LSa', 'LSc2', 'LSc4', 'GBa', 'GBc', 'Ta', 'Tc2', 'Tc4',
                      'Exposure', 'Gut', 'LegLace', 'Turn', 'Recovery', 'Pushout', 'Passive', 'Violation',
                      'oHIa', 'oHIc2', 'oHIc4', 'oHOa', 'oHOc2', 'oHOc4', 'oDa', 'oDc2', 'oDc4', 'oLSa', 'oLSc2', 'oLSc4', 'oGBa', 'oGBc', 'oTa', 'oTc2', 'oTc4',
                      'oExposure', 'oGut', 'oLegLace', 'oTurn', 'oRecovery', 'oPushout', 'oPassive', 'oViolation',
                      'HIrate', 'HOrate', 'Drate', 'LSrate', 'GBrate', 'Trate', 'NPF', 'APM', 'VS',
                      'oHIrate', 'oHOrate', 'oDrate', 'oLSrate', 'oGBrate', 'oTrate', 'oNPF', 'oAPM', 'oVS']

        data = [self.x.matchID_value, self.controller.shared_data['blue_name'].get(), self.controller.shared_data['red_name'].get(),
                self.controller.shared_data['blue_team'].get(), self.controller.shared_data['red_team'].get(), self.controller.shared_data['weight_class'].get(), datetime.date.today(),
                self.x.result_abb.get(), self.x.blue_score.get(), self.x.red_score.get(), self.x.blue_score.get() - self.x.red_score.get(), self.x.main_clock.timestr.get(),
                self.x.bhia, self.x.bhic2, self.x.bhic4, self.x.bhoa, self.x.bhoc2, self.x.bhoc4, self.x.bda, self.x.bdc2, self.x.bdc4, self.x.blsa, self.x.blsc2, self.x.blsc4,
                self.x.bgba, self.x.bgbc, self.x.bta, self.x.btc2, self.x.btc4, self.x.bexposure, self.x.bgut, self.x.bleglace, self.x.bturn, self.x.brecovery, self.x.bpushout, self.x.bpassive, self.x.btv,
                self.x.rhia, self.x.rhic2, self.x.rhic4, self.x.rhoa, self.x.rhoc2, self.x.rhoc4, self.x.rda, self.x.rdc2, self.x.rdc4, self.x.rlsa, self.x.rlsc2, self.x.rlsc4,
                self.x.rgba, self.x.rgbc, self.x.rta, self.x.rtc2, self.x.rtc4, self.x.rexposure, self.x.rgut, self.x.rleglace, self.x.rturn, self.x.rrecovery, self.x.rpushout, self.x.rpassive, self.x.rtv,
                self.x.bhi_rate.get(), self.x.bho_rate.get(), self.x.bd_rate.get(), self.x.bls_rate.get(), self.x.bgb_rate.get(), self.x.bt_rate.get(), self.x.b_npf.get(), self.x.b_action.get(), self.x.b_vs.get(),
                self.x.rhi_rate.get(), self.x.rho_rate.get(), self.x.rd_rate.get(), self.x.rls_rate.get(), self.x.rgb_rate.get(), self.x.rt_rate.get(), self.x.r_npf.get(), self.x.r_action.get(), self.x.r_vs.get()]

        data2 = [self.x.matchID_value + '*', self.controller.shared_data['red_name'].get(), self.controller.shared_data['blue_name'].get(),
                 self.controller.shared_data['red_team'].get(), self.controller.shared_data['blue_team'].get(), self.controller.shared_data['weight_class'].get(), datetime.date.today(),
                 self.x.result_opp_abb.get(), self.x.red_score.get(), self.x.blue_score.get(), self.x.red_score.get() - self.x.blue_score.get(), self.x.main_clock.timestr.get(),
                 self.x.rhia, self.x.rhic2, self.x.rhic4, self.x.rhoa, self.x.rhoc2, self.x.rhoc4, self.x.rda, self.x.rdc2, self.x.rdc4, self.x.rlsa, self.x.rlsc2, self.x.rlsc4,
                 self.x.rgba, self.x.rgbc, self.x.rta, self.x.rtc2, self.x.rtc4, self.x.rexposure, self.x.rgut, self.x.rleglace, self.x.rturn, self.x.rrecovery, self.x.rpushout, self.x.rpassive, self.x.rtv,
                 self.x.bhia, self.x.bhic2, self.x.bhic4, self.x.bhoa, self.x.bhoc2, self.x.bhoc4, self.x.bda, self.x.bdc2, self.x.bdc4, self.x.blsa, self.x.blsc2, self.x.blsc4,
                 self.x.bgba, self.x.bgbc, self.x.bta, self.x.btc2, self.x.btc4, self.x.bexposure, self.x.bgut, self.x.bleglace, self.x.bturn, self.x.brecovery, self.x.bpushout, self.x.bpassive, self.x.btv,
                 self.x.rhi_rate.get(), self.x.rho_rate.get(), self.x.rd_rate.get(), self.x.rls_rate.get(), self.x.rgb_rate.get(), self.x.rt_rate.get(), self.x.r_npf.get(), self.x.r_action.get(), self.x.r_vs.get(),
                 self.x.bhi_rate.get(), self.x.bho_rate.get(), self.x.bd_rate.get(), self.x.bls_rate.get(), self.x.bgb_rate.get(), self.x.bt_rate.get(), self.x.b_npf.get(), self.x.b_action.get(), self.x.b_vs.get()]


        """
        Uploads all data to database instances of Matches.
        This includes two uploads, one for the main match and a secondary one
        for the opponent version of the match. The second match has and '*' suffix.
        """
        self.textbox.config(state=tk.NORMAL)

        m1 = FS_Match.objects.get(matchID=data[0])
        m1.weight = data[5]
        m1.save()
        m1.date = data[6]
        m1.save()
        m1.result = data[7]
        m1.save()
        m1.focus_score = data[8]
        m1.save()
        m1.opp_score = data[9]
        m1.save()
        m1.mov = data[10]
        m1.save()
        m1.duration = data[11]
        m1.save()
        m1.hia = data[12]
        m1.save()
        m1.hic2 = data[13]
        m1.save()
        m1.hic4 = data[14]
        m1.save()
        m1.hoa = data[15]
        m1.save()
        m1.hoc2 = data[16]
        m1.save()
        m1.hoc4 = data[17]
        m1.save()
        m1.da = data[18]
        m1.save()
        m1.dc2 = data[19]
        m1.save()
        m1.dc4 = data[20]
        m1.save()
        m1.lsa = data[21]
        m1.save()
        m1.lsc2 = data[22]
        m1.save()
        m1.lsc4 = data[23]
        m1.save()
        m1.gba = data[24]
        m1.save()
        m1.gbc2 = data[25]
        m1.save()
        m1.ta = data[26]
        m1.save()
        m1.tc2 = data[27]
        m1.save()
        m1.tc4 = data[28]
        m1.save()
        m1.exposure = data[29]
        m1.save()
        m1.gut = data[30]
        m1.save()
        m1.leg_lace = data[31]
        m1.save()
        m1.turn = data[32]
        m1.save()
        m1.recovery = data[33]
        m1.save()
        m1.pushout = data[34]
        m1.save()
        m1.passive = data[35]
        m1.save()
        m1.violation = data[36]
        m1.save()
        m1.opp_hia = data[37]
        m1.save()
        m1.opp_hic2 = data[38]
        m1.save()
        m1.opp_hic4 = data[39]
        m1.save()
        m1.opp_hoa = data[40]
        m1.save()
        m1.opp_hoc2 = data[41]
        m1.save()
        m1.opp_hoc4 = data[42]
        m1.save()
        m1.opp_da = data[43]
        m1.save()
        m1.opp_dc2 = data[44]
        m1.save()
        m1.opp_dc4 = data[45]
        m1.save()
        m1.opp_lsa = data[46]
        m1.save()
        m1.opp_lsc2 = data[47]
        m1.save()
        m1.opp_lsc4 = data[48]
        m1.save()
        m1.opp_gba = data[49]
        m1.save()
        m1.opp_gbc2 = data[50]
        m1.save()
        m1.opp_ta = data[51]
        m1.save()
        m1.opp_tc2 = data[52]
        m1.save()
        m1.opp_tc4 = data[53]
        m1.save()
        m1.opp_exposure = data[54]
        m1.save()
        m1.opp_gut = data[55]
        m1.save()
        m1.opp_leg_lace = data[56]
        m1.save()
        m1.opp_turn = data[57]
        m1.save()
        m1.opp_recovery = data[58]
        m1.save()
        m1.opp_pushout = data[59]
        m1.save()
        m1.opp_passive = data[60]
        m1.save()
        m1.opp_violation = data[61]
        m1.save()
        m1.hi_rate = data[62]
        m1.save()
        m1.ho_rate = data[63]
        m1.save()
        m1.d_rate = data[64]
        m1.save()
        m1.ls_rate = data[65]
        m1.save()
        m1.gb_rate = data[66]
        m1.save()
        m1.t_rate = data[67]
        m1.save()
        m1.npf = data[68]
        m1.save()
        m1.apm = data[69]
        m1.save()
        m1.vs = data[70]
        m1.save()
        m1.opp_hi_rate = data[71]
        m1.save()
        m1.opp_ho_rate = data[72]
        m1.save()
        m1.opp_d_rate = data[73]
        m1.save()
        m1.opp_ls_rate = data[74]
        m1.save()
        m1.opp_gb_rate = data[75]
        m1.save()
        m1.opp_t_rate = data[76]
        m1.save()
        m1.opp_npf = data[77]
        m1.save()
        m1.opp_apm = data[78]
        m1.save()
        m1.opp_vs = data[79]
        m1.save()

        # "match2"
        m2 = FS_Match.objects.get(matchID=data2[0])
        m2.weight = data2[5]
        m2.save()
        m2.date = data2[6]
        m2.save()
        m2.result = data2[7]
        m2.save()
        m2.focus_score = data2[8]
        m2.save()
        m2.opp_score = data2[9]
        m2.save()
        m2.mov = data2[10]
        m2.save()
        m2.duration = data2[11]
        m2.save()
        m2.hia = data2[12]
        m2.save()
        m2.hic2 = data2[13]
        m2.save()
        m2.hic4 = data2[14]
        m2.save()
        m2.hoa = data2[15]
        m2.save()
        m2.hoc2 = data2[16]
        m2.save()
        m2.hoc4 = data2[17]
        m2.save()
        m2.da = data2[18]
        m2.save()
        m2.dc2 = data2[19]
        m2.save()
        m2.dc4 = data2[20]
        m2.save()
        m2.lsa = data2[21]
        m2.save()
        m2.lsc2 = data2[22]
        m2.save()
        m2.lsc4 = data2[23]
        m2.save()
        m2.gba = data2[24]
        m2.save()
        m2.gbc2 = data2[25]
        m2.save()
        m2.ta = data2[26]
        m2.save()
        m2.tc2 = data2[27]
        m2.save()
        m2.tc4 = data2[28]
        m2.save()
        m2.exposure = data2[29]
        m2.save()
        m2.gut = data2[30]
        m2.save()
        m2.leg_lace = data2[31]
        m2.save()
        m2.turn = data2[32]
        m2.save()
        m2.recovery = data2[33]
        m2.save()
        m2.pushout = data2[34]
        m2.save()
        m2.passive = data2[35]
        m2.save()
        m2.violation = data2[36]
        m2.save()
        m2.opp_hia = data2[37]
        m2.save()
        m2.opp_hic2 = data2[38]
        m2.save()
        m2.opp_hic4 = data2[39]
        m2.save()
        m2.opp_hoa = data2[40]
        m2.save()
        m2.opp_hoc2 = data2[41]
        m2.save()
        m2.opp_hoc4 = data2[42]
        m2.save()
        m2.opp_da = data2[43]
        m2.save()
        m2.opp_dc2 = data2[44]
        m2.save()
        m2.opp_dc4 = data2[45]
        m2.save()
        m2.opp_lsa = data2[46]
        m2.save()
        m2.opp_lsc2 = data2[47]
        m2.save()
        m2.opp_lsc4 = data2[48]
        m2.save()
        m2.opp_gba = data2[49]
        m2.save()
        m2.opp_gbc2 = data2[50]
        m2.save()
        m2.opp_ta = data2[51]
        m2.save()
        m2.opp_tc2 = data2[52]
        m2.save()
        m2.opp_tc4 = data2[53]
        m2.save()
        m2.opp_exposure = data2[54]
        m2.save()
        m2.opp_gut = data2[55]
        m2.save()
        m2.opp_leg_lace = data2[56]
        m2.save()
        m2.opp_turn = data2[57]
        m2.save()
        m2.opp_recovery = data2[58]
        m2.save()
        m2.opp_pushout = data2[59]
        m2.save()
        m2.opp_passive = data2[60]
        m2.save()
        m2.opp_violation = data2[61]
        m2.save()
        m2.hi_rate = data2[62]
        m2.save()
        m2.ho_rate = data2[63]
        m2.save()
        m2.d_rate = data2[64]
        m2.save()
        m2.ls_rate = data2[65]
        m2.save()
        m2.gb_rate = data2[66]
        m2.save()
        m2.t_rate = data2[67]
        m2.save()
        m2.npf = data2[68]
        m2.save()
        m2.apm = data2[69]
        m2.save()
        m2.vs = data2[70]
        m2.save()
        m2.opp_hi_rate = data2[71]
        m2.save()
        m2.opp_ho_rate = data2[72]
        m2.save()
        m2.opp_d_rate = data2[73]
        m2.save()
        m2.opp_ls_rate = data2[74]
        m2.save()
        m2.opp_gb_rate = data2[75]
        m2.save()
        m2.opp_t_rate = data2[76]
        m2.save()
        m2.opp_npf = data2[77]
        m2.save()
        m2.opp_apm = data2[78]
        m2.save()
        m2.opp_vs = data2[79]
        m2.save()

        self.textbox.insert(tk.END, '\n---------\n', 'center-tag')
        self.textbox.insert(tk.END, 'Matches uploaded to database', 'center-tag')
        self.textbox.insert(tk.END, '\n---------\n', 'center-tag')

        # matchdata = pd.DataFrame(columns=rawcolumns)
        # matchdata = matchdata.append(pd.Series(data, index=rawcolumns), ignore_index=True)
        # matchdata = matchdata.append(pd.Series(data2, index=rawcolumns), ignore_index=True)
        # matchdata = matchdata.set_index('MatchID')

        backend.ranking_function(self)
        self.textbox.insert(tk.END, '\n---------\n', 'center-tag')
        # self.textbox.insert(tk.END, 'Wrestlers rating updated in csv', 'center-tag')
        # self.textbox.insert(tk.END, '\n---------\n', 'center-tag')
        # matchdata save
        # matchdata.to_csv('collection/stats/matchdata.csv', mode='a', header=False)
        # self.textbox.insert(tk.END, 'Matchdata saved to csv', 'center-tag')
        # self.textbox.insert(tk.END, '\n---------\n', 'center-tag')
        # self.x.ts_df.to_csv('collection/stats/timeseries.csv', mode='a', header=False)
        # self.textbox.insert(tk.END, 'Timeseries saved to csv', 'center-tag')
        # self.textbox.insert(tk.END, '\n---------', 'center-tag')
        self.textbox.configure(state=tk.DISABLED)


def main():
    """
    Instantiaizes main app class.
    """
    app = Collector()
    app.mainloop()


if __name__ == '__main__':
    main()
