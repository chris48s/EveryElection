# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-05 16:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elections', '0051_auto_20181005_1618'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='moderationhistory',
            options={'get_latest_by': 'modified', 'ordering': ('election', '-modified'), 'verbose_name_plural': 'Moderation History'},
        ),
    ]
