from django.db import models
from django.contrib.auth.models import User
from vws_main.models import FS_Wrestler
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teamname = models.CharField(max_length=250)
    image = models.ImageField(default='profile_pics/mini.png', upload_to='profile_pics')
    roster57 = models.ForeignKey(FS_Wrestler, on_delete=models.CASCADE,
                                 related_name='r57', default='Placeholder')
    roster61 = models.ForeignKey(FS_Wrestler, on_delete=models.CASCADE,
                                 related_name='r61', default='Placeholder')
    roster65 = models.ForeignKey(FS_Wrestler, on_delete=models.CASCADE,
                                 related_name='r65', default='Placeholder')
    roster70 = models.ForeignKey(FS_Wrestler, on_delete=models.CASCADE,
                                 related_name='r70', default='Placeholder')
    roster74 = models.ForeignKey(FS_Wrestler, on_delete=models.CASCADE,
                                 related_name='r74', default='Placeholder')
    roster79 = models.ForeignKey(FS_Wrestler, on_delete=models.CASCADE,
                                 related_name='r79', default='Placeholder')
    roster86 = models.ForeignKey(FS_Wrestler, on_delete=models.CASCADE,
                                 related_name='r86', default='Placeholder')
    roster92 = models.ForeignKey(FS_Wrestler, on_delete=models.CASCADE,
                                 related_name='r92', default='Placeholder')
    roster97 = models.ForeignKey(FS_Wrestler, on_delete=models.CASCADE,
                                 related_name='r97', default='Placeholder')
    roster125 = models.ForeignKey(FS_Wrestler, on_delete=models.CASCADE,
                                 related_name='r125', default='Placeholder')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 200 or img.width > 200:
            output_size = (200, 200)
            img.thumbnail(output_size)
            img.save(self.image.path)

