from django.db import models
from django.conf import settings


class Wrestler(models.Model):
    name = models.CharField(max_length=140, primary_key=True)
    team = models.CharField(max_length=140)
    eligibility = models.CharField(max_length=140)
    rating = models.IntegerField()
    competitions = models.CharField(max_length=140, default='o')

    def __str_(self):
        return self.name


class Matchdata(models.Model):
    matchID = models.CharField(max_length=140, primary_key=True, unique=True)
    date = models.CharField(max_length=140)
    blue = models.CharField(max_length=140)
    red = models.CharField(max_length=140)
    blue_score = models.IntegerField()
    red_score = models.IntegerField()
    result = models.CharField(max_length=140)

    def __str_(self):
        return self.matchID


class Timeseries(models.Model):
    matchID = models.ForeignKey(Matchdata, on_delete=models.CASCADE, related_name='events')
    event_num = models.IntegerField()
    event_lab = models.CharField(max_length=140)
    event_time = models.DecimalField(max_digits=10, decimal_places=2)
    blue = models.CharField(max_length=140)
    red = models.CharField(max_length=140)

    def __str_(self):
        return self.matchID
