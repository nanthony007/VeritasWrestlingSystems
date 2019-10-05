from django.db import models
from django.contrib.auth.models import User
from vws_main.models import FS_Wrestler
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teamname = models.CharField(max_length=250)
    image = models.ImageField(default='profile_pics/mini.png', upload_to='profile_pics')
    roster = models.ManyToManyField(FS_Wrestler, related_name='roster')

    def __str__(self):
        return self.name
    

    def __str__(self):
        return r'{self.user.username} Profile'

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 200 or img.width > 200:
            output_size = (200, 200)
            img.thumbnail(output_size)
            img.save(self.image.path)
