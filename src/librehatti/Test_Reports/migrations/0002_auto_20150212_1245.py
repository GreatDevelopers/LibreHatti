# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Test_Reports', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test_reports',
            name='mix',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
