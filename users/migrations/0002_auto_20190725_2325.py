# Generated by Django 2.1.5 on 2019-07-26 03:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vws_main', '0006_remove_fs_match_opp_gbc4'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='roster57',
            field=models.ForeignKey(default='Yianni Diakomihalis', on_delete=django.db.models.deletion.CASCADE, related_name='r57', to='vws_main.FS_Wrestler'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='profile_pics/mini.png', upload_to='profile_pics'),
        ),
    ]
