# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0033_organisationname'),
    ]

    operations = [
        migrations.RunSQL("""
            INSERT INTO organisations_organisationname (
                official_name, common_name, slug, election_name,
                start_date, end_date, organisation_id
            ) (SELECT
                official_name, common_name, slug, election_name,
                start_date, end_date, id
            FROM organisations_organisation);""",

            reverse_sql="DELETE FROM organisations_organisationname;"
        ),
    ]
