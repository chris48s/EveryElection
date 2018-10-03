# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def load_init_data(apps, schema_editor):
    ModerationStatus = apps.get_model("elections", "ModerationStatus")
    recs = [
        ModerationStatus(
            short_title="Suggested",
            long_title="Suggested by an anonymous user"
        ),
        ModerationStatus(
            short_title="Rejected",
            long_title="Rejected by a moderator"
        ),
        ModerationStatus(
            short_title="Approved",
            long_title="Approved by a moderator"
        ),
        ModerationStatus(
            short_title="Deleted",
            long_title="Deleted (because it was added in error)"
        ),
    ]
    for rec in recs:
        rec.save()


def delete_init_data(apps, schema_editor):
    ModerationStatus = apps.get_model("elections", "ModerationStatus")
    ModerationStatus.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('elections', '0047_moderationstatus'),
    ]

    operations = [
        migrations.RunPython(load_init_data, delete_init_data),
    ]
