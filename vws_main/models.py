from django.db import models


class Wrestler(models.Model):
    athlete = models.CharField(max_length=140)
    team = models.CharField(max_length=140)
    eligibility = models.CharField(max_length=140)
    rating = models.IntegerField()

    def __str_(self):
        return self.athlete


class Timeseries(models.Model):
    matchID = models.CharField(max_length=140)
    event_num = models.IntegerField()
    event_lab = models.CharField(max_length=140)
    event_time = models.DecimalField(max_digits=10, decimal_places=2)
    blue = models.CharField(max_length=140)
    red = models.CharField(max_length=140)

    def __str_(self):
        return self.matchID
