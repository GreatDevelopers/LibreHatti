# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Test_Reports', '0003_auto_20150213_1727'),
    ]

    operations = [
        migrations.AddField(
            model_name='test_reports',
            name='City',
            field=models.CharField(default=datetime.datetime(2015, 2, 17, 11, 55, 30, 590014, tzinfo=utc), max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='test_report_descriptions',
            name='Start_Date',
            field=models.DateField(verbose_name=b'Cube Test'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test_reports',
            name='Refernce_Date',
            field=models.DateField(verbose_name=b'Letter Date'),
            preserve_default=True,
        ),
    ]
