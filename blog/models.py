from django.db import models
import datetime

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=250, primary_key=True, unique=True)
    content = models.FileField()
    date = models.DateField(auto_now_add=datetime.datetime.today)
    slug = models.SlugField(default=title)

    def __str_(self):
        return self.title
