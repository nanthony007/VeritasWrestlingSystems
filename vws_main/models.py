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
