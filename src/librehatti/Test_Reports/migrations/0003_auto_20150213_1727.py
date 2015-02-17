# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Test_Reports', '0002_auto_20150212_1245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test_report_descriptions',
            name='mix',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
    ]
