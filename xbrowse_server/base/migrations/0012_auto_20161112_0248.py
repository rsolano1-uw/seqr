# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-11-12 07:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_auto_20161110_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='individual',
            name='phenotips_features',
            field=models.TextField(blank=True, default=b'', null=True),
        ),
        migrations.AlterField(
            model_name='family',
            name='analysis_status_date_saved',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
