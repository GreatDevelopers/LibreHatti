# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voucher', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test_Report_Descriptions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Start_Date', models.DateField(verbose_name=b'starting date')),
                ('Description', models.CharField(max_length=200)),
                ('Strength', models.CharField(max_length=20)),
                ('mix', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Test_Reports',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Voucher', models.CharField(max_length=200)),
                ('Client', models.CharField(max_length=200)),
                ('mix', models.IntegerField()),
                ('Address', models.CharField(max_length=200)),
                ('Subject', models.CharField(max_length=200)),
                ('Refernce_no', models.CharField(max_length=200)),
                ('Refernce_Date', models.DateField(verbose_name=b'starting date')),
                ('Testing_Date', models.DateField(verbose_name=b'Test Date')),
                ('Session', models.ForeignKey(to='voucher.FinancialSession')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='test_report_descriptions',
            name='report_id',
            field=models.ForeignKey(to='Test_Reports.Test_Reports'),
            preserve_default=True,
        ),
    ]
