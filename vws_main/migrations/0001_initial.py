# Generated by Django 2.1.5 on 2019-01-12 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TimeSeries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matchID', models.CharField(max_length=140)),
                ('event_num', models.IntegerField()),
                ('event_lab', models.CharField(max_length=140)),
                ('event_time', models.DecimalField(decimal_places=1, max_digits=10)),
                ('blue', models.CharField(max_length=140)),
                ('red', models.CharField(max_length=140)),
            ],
        ),
        migrations.CreateModel(
            name='Wrestler',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('athlete', models.CharField(max_length=140)),
                ('team', models.CharField(max_length=140)),
                ('eligibility', models.CharField(max_length=140)),
                ('rating', models.IntegerField()),
            ],
        ),
    ]