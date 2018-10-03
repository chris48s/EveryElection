# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def copy_status_data(apps, schema_editor):
    ElectionModerationStatus = apps.get_model(
        "elections", "ElectionModerationStatus")
    Election = apps.get_model("elections", "Election")
    ModerationStatus = apps.get_model("elections", "ModerationStatus")
    for election in Election.private_objects.all():
        rec = (ElectionModerationStatus(
            election=election,
            status=ModerationStatus.objects.all().get(
                short_title__iexact=election.suggested_status
            )
        ))
        rec.save()


def delete_status_data(apps, schema_editor):
    ElectionModerationStatus = apps.get_model(
        "elections", "ElectionModerationStatus")
    ElectionModerationStatus.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('elections', '0050_auto_20181003_1100'),
    ]

    operations = [
        migrations.RunPython(copy_status_data, delete_status_data),
    ]
