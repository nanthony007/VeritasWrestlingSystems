# Generated by Django 2.1.7 on 2019-10-10 03:45

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vws_main', '0007_1_report'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='report',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location='/media/reports/'), upload_to=''),
        ),
    ]