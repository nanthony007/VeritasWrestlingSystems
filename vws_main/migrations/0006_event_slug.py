# Generated by Django 2.1.5 on 2019-01-18 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vws_main', '0005_auto_20190117_1152'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='slug',
            field=models.SlugField(default=models.CharField(max_length=140)),
        ),
    ]