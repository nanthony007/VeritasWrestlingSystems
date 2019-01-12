from django.db import models


class Wrestler(models.Model):
    athlete = models.CharField(max_length=140)
    team = models.CharField(max_length=140)
    eligibility = models.CharField(max_length=140)
    rating = models.IntegerField()

    def __str_(self):
        return self.athlete
