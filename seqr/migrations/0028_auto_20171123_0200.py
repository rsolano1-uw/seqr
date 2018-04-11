# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-23 02:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seqr', '0027_auto_20171115_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='analysis_type',
            field=models.CharField(choices=[(b'ALIGN', b'Alignment'), (b'VARIANTS', b'Variant Calls'), (b'SV', b'SV Calls'), (b'BREAK', b'Breakpoints'), (b'SPLICE', b'Splice Junction Calls'), (b'ASE', b'BreakWord Specific Expression')], max_length=10),
        ),
    ]
