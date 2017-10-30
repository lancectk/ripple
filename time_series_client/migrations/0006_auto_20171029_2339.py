# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-29 23:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('time_series_client', '0005_auto_20171029_0249'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useredgeweight',
            old_name='edge_id',
            new_name='source_vertex_id',
        ),
        migrations.AddField(
            model_name='useredgeweight',
            name='target_vertex_id',
            field=models.CharField(default=None, max_length=64),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='useredgeweight',
            unique_together=set([('user_id', 'source_vertex_id', 'target_vertex_id', 'weight_id')]),
        ),
    ]
