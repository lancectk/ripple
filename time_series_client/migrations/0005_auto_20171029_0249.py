# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-29 02:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('time_series_client', '0004_auto_20171029_0208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graphversion',
            name='version_id',
            field=models.IntegerField(),
        ),
    ]
