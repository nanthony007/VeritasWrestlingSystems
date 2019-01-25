from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify

class Team(models.Model):
    name = models.CharField(max_length=250, primary_key=True, unique=True)
    abbreviation = models.CharField(max_length=20)
    slug = models.SlugField(default=name)

    def __str_(self):
        return self.name


class Wrestler(models.Model):
    name = models.CharField(max_length=140, primary_key=True, unique=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_name')
    eligibility = models.CharField(max_length=140)
    rating = models.IntegerField()
    competitions = models.CharField(max_length=500, default=' ')
    slug = models.SlugField(default=name)

    def __str_(self):
        return self.name


class Matchdata(models.Model):
    matchID = models.CharField(max_length=140, primary_key=True, unique=True)
    date = models.CharField(max_length=140)
    focus = models.ForeignKey(Wrestler, on_delete=models.CASCADE, related_name='focus_wrestler')
    focus_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='focus_team_name')
    opponent = models.ForeignKey(Wrestler, on_delete=models.CASCADE, related_name='opp_wrestler')
    opp_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='opp_team_name')
    focus_score = models.IntegerField()
    opp_score = models.IntegerField()
    result = models.CharField(max_length=140)
    weight = models.IntegerField()
    mov = models.IntegerField()
    duration = models.DecimalField(max_digits=15, decimal_places=2)
    hia = models.IntegerField()
    hic = models.IntegerField()
    hoa = models.IntegerField()
    hoc = models.IntegerField()
    da = models.IntegerField()
    dc = models.IntegerField()
    lsa = models.IntegerField()
    lsc = models.IntegerField()
    gba = models.IntegerField()
    gbc = models.IntegerField()
    ta = models.IntegerField()
    tc = models.IntegerField()
    su = models.IntegerField()
    e = models.IntegerField()
    r = models.IntegerField()
    cut = models.IntegerField()
    bd = models.IntegerField()
    mr = models.IntegerField()
    nf2 = models.IntegerField()
    nf4 = models.IntegerField()
    caution = models.IntegerField()
    tv = models.IntegerField()
    rt = models.IntegerField()
    opp_hia = models.IntegerField()
    opp_hic = models.IntegerField()
    opp_hoa = models.IntegerField()
    opp_hoc = models.IntegerField()
    opp_da = models.IntegerField()
    opp_dc = models.IntegerField()
    opp_lsa = models.IntegerField()
    opp_lsc = models.IntegerField()
    opp_gba = models.IntegerField()
    opp_gbc = models.IntegerField()
    opp_ta = models.IntegerField()
    opp_tc = models.IntegerField()
    opp_su = models.IntegerField()
    opp_e = models.IntegerField()
    opp_r = models.IntegerField()
    opp_cut = models.IntegerField()
    opp_bd = models.IntegerField()
    opp_mr = models.IntegerField()
    opp_nf2 = models.IntegerField()
    opp_nf4 = models.IntegerField()
    opp_caution = models.IntegerField()
    opp_tv = models.IntegerField()
    opp_rt = models.IntegerField()
    hi_rate = models.DecimalField(max_digits=15, decimal_places=2)
    ho_rate = models.DecimalField(max_digits=15, decimal_places=2)
    d_rate = models.DecimalField(max_digits=15, decimal_places=2)
    ls_rate = models.DecimalField(max_digits=15, decimal_places=2)
    gb_rate = models.DecimalField(max_digits=15, decimal_places=2)
    t_rate = models.DecimalField(max_digits=15, decimal_places=2)
    td_rate = models.DecimalField(max_digits=15, decimal_places=2)
    e_rate = models.DecimalField(max_digits=15, decimal_places=2)
    ride_rate = models.DecimalField(max_digits=15, decimal_places=2)
    apm = models.DecimalField(max_digits=15, decimal_places=2)
    vs = models.DecimalField(max_digits=15, decimal_places=2)
    opp_hi_rate = models.DecimalField(max_digits=15, decimal_places=2)
    opp_ho_rate = models.DecimalField(max_digits=15, decimal_places=2)
    opp_d_rate = models.DecimalField(max_digits=15, decimal_places=2)
    opp_ls_rate = models.DecimalField(max_digits=15, decimal_places=2)
    opp_gb_rate = models.DecimalField(max_digits=15, decimal_places=2)
    opp_t_rate = models.DecimalField(max_digits=15, decimal_places=2)
    opp_td_rate = models.DecimalField(max_digits=15, decimal_places=2)
    opp_e_rate = models.DecimalField(max_digits=15, decimal_places=2)
    opp_ride_rate = models.DecimalField(max_digits=15, decimal_places=2)
    opp_apm = models.DecimalField(max_digits=15, decimal_places=2)
    opp_vs = models.DecimalField(max_digits=15, decimal_places=2)


    def __str_(self):
        return self.matchID


class Timeseries(models.Model):
    matchID = models.ForeignKey(Matchdata, on_delete=models.CASCADE, related_name='actions')
    event_num = models.IntegerField()
    event_lab = models.CharField(max_length=140)
    event_time = models.DecimalField(max_digits=10, decimal_places=2)
    blue = models.CharField(max_length=140)
    red = models.CharField(max_length=140)

    def __str_(self):
        return self.matchID


class Event(models.Model):
    name = models.CharField(max_length=140)
    matches = models.ManyToManyField(Matchdata, related_name='events')
    slug = models.SlugField(default=name)

    def __str_(self):
        return self.name
