# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-18 10:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elections', '0039_auto_20180309_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='election',
            name='seats_contested',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='election',
            name='seats_total',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]