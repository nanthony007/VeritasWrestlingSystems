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
    blue = models.ForeignKey(Wrestler, on_delete=models.CASCADE, related_name='blue_wrestler')
    blue_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='blue_team_name')
    red = models.ForeignKey(Wrestler, on_delete=models.CASCADE, related_name='red_wrestler')
    red_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='red_team_name')
    blue_score = models.IntegerField()
    red_score = models.IntegerField()
    result = models.CharField(max_length=140)
    weight = models.IntegerField()
    mov = models.IntegerField()
    duration = models.DecimalField(max_digits=15, decimal_places=2)
    blue_hia = models.IntegerField()
    blue_hic = models.IntegerField()
    blue_hoa = models.IntegerField()
    blue_hoc = models.IntegerField()
    blue_da = models.IntegerField()
    blue_dc = models.IntegerField()
    blue_lsa = models.IntegerField()
    blue_lsc = models.IntegerField()
    blue_gba = models.IntegerField()
    blue_gbc = models.IntegerField()
    blue_ta = models.IntegerField()
    blue_tc = models.IntegerField()
    blue_su = models.IntegerField()
    blue_e = models.IntegerField()
    blue_r = models.IntegerField()
    blue_cut = models.IntegerField()
    blue_bd = models.IntegerField()
    blue_mr = models.IntegerField()
    blue_nf2 = models.IntegerField()
    blue_nf4 = models.IntegerField()
    blue_caution = models.IntegerField()
    blue_tv = models.IntegerField()
    blue_rt = models.IntegerField()
    red_hia = models.IntegerField()
    red_hic = models.IntegerField()
    red_hoa = models.IntegerField()
    red_hoc = models.IntegerField()
    red_da = models.IntegerField()
    red_dc = models.IntegerField()
    red_lsa = models.IntegerField()
    red_lsc = models.IntegerField()
    red_gba = models.IntegerField()
    red_gbc = models.IntegerField()
    red_ta = models.IntegerField()
    red_tc = models.IntegerField()
    red_su = models.IntegerField()
    red_e = models.IntegerField()
    red_r = models.IntegerField()
    red_cut = models.IntegerField()
    red_bd = models.IntegerField()
    red_mr = models.IntegerField()
    red_nf2 = models.IntegerField()
    red_nf4 = models.IntegerField()
    red_caution = models.IntegerField()
    red_tv = models.IntegerField()
    red_rt = models.IntegerField()
    blue_hi_rate = models.DecimalField(max_digits=15, decimal_places=2)
    blue_ho_rate = models.DecimalField(max_digits=15, decimal_places=2)
    blue_d_rate = models.DecimalField(max_digits=15, decimal_places=2)
    blue_ls_rate = models.DecimalField(max_digits=15, decimal_places=2)
    blue_gb_rate = models.DecimalField(max_digits=15, decimal_places=2)
    blue_t_rate = models.DecimalField(max_digits=15, decimal_places=2)
    blue_td_rate = models.DecimalField(max_digits=15, decimal_places=2)
    blue_e_rate = models.DecimalField(max_digits=15, decimal_places=2)
    blue_ride_rate = models.DecimalField(max_digits=15, decimal_places=2)
    blue_apm = models.DecimalField(max_digits=15, decimal_places=2)
    blue_vs = models.DecimalField(max_digits=15, decimal_places=2)
    red_hi_rate = models.DecimalField(max_digits=15, decimal_places=2)
    red_ho_rate = models.DecimalField(max_digits=15, decimal_places=2)
    red_d_rate = models.DecimalField(max_digits=15, decimal_places=2)
    red_ls_rate = models.DecimalField(max_digits=15, decimal_places=2)
    red_gb_rate = models.DecimalField(max_digits=15, decimal_places=2)
    red_t_rate = models.DecimalField(max_digits=15, decimal_places=2)
    red_td_rate = models.DecimalField(max_digits=15, decimal_places=2)
    red_e_rate = models.DecimalField(max_digits=15, decimal_places=2)
    red_ride_rate = models.DecimalField(max_digits=15, decimal_places=2)
    red_apm = models.DecimalField(max_digits=15, decimal_places=2)
    red_vs = models.DecimalField(max_digits=15, decimal_places=2)


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
