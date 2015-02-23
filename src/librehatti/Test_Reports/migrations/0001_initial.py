# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voucher', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Soil_building',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Voucher', models.CharField(max_length=200)),
                ('Date_of_Testing', models.DateField(verbose_name=b'Date of Testing')),
                ('Type_of_str', models.CharField(max_length=200)),
                ('Latitude_N', models.CharField(max_length=200)),
                ('Longitude_E', models.CharField(max_length=200)),
                ('Presence_1', models.CharField(max_length=200)),
                ('Presence_2', models.CharField(max_length=200)),
                ('Submitted_1', models.CharField(max_length=200)),
                ('Submitted_2', models.CharField(max_length=200)),
                ('Submitted_3', models.CharField(max_length=200)),
                ('Site_Name', models.CharField(max_length=200)),
                ('Bore_Hole', models.CharField(max_length=200)),
                ('Water_Table', models.CharField(max_length=200)),
                ('Wall_Dt', models.CharField(max_length=200)),
                ('Wall_B', models.CharField(max_length=200)),
                ('Col_Df', models.CharField(max_length=200)),
                ('Col_L', models.CharField(max_length=200)),
                ('Col_B', models.CharField(max_length=200)),
                ('Gama_wall', models.CharField(max_length=200)),
                ('Wall_C', models.CharField(max_length=200)),
                ('Wall_Phay', models.CharField(max_length=200)),
                ('Wall_Phay_Fe', models.CharField(max_length=200)),
                ('Wall_Nc', models.CharField(max_length=200)),
                ('Wall_Nq', models.CharField(max_length=200)),
                ('Wall_Ny', models.CharField(max_length=200)),
                ('Wall_Sc', models.CharField(max_length=200)),
                ('Wall_Sq', models.CharField(max_length=200)),
                ('Wall_Sy', models.CharField(max_length=200)),
                ('Wall_dc', models.CharField(max_length=200)),
                ('Wall_dq_dy', models.CharField(max_length=200)),
                ('Wall_w', models.CharField(max_length=200)),
                ('Wall_peq', models.CharField(max_length=200)),
                ('Wall_Total', models.CharField(max_length=200)),
                ('Wall_T_2', models.CharField(max_length=200)),
                ('Col_Sc', models.CharField(max_length=200)),
                ('Col_Sq', models.CharField(max_length=200)),
                ('Col_Sy', models.CharField(max_length=200)),
                ('Col_dc', models.CharField(max_length=200)),
                ('Col_dq_dy', models.CharField(max_length=200)),
                ('Col_peq', models.CharField(max_length=200)),
                ('Col_Total', models.CharField(max_length=200)),
                ('Col_T_2', models.CharField(max_length=200)),
                ('Wall_N_V', models.CharField(max_length=200)),
                ('Wall_S', models.CharField(max_length=200)),
                ('Wall_Value', models.CharField(max_length=200)),
                ('Wall_Net_V', models.CharField(max_length=200)),
                ('Wall_G_V', models.CharField(max_length=200)),
                ('Col_N_V', models.CharField(max_length=200)),
                ('Col_Value', models.CharField(max_length=200)),
                ('Col_Net_V', models.CharField(max_length=200)),
                ('Col_G_V', models.CharField(max_length=200)),
                ('Session', models.ForeignKey(to='voucher.FinancialSession')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Soil_building_des',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Dt', models.CharField(max_length=200)),
                ('Ob_Pr', models.CharField(max_length=200)),
                ('Corr_F', models.CharField(max_length=200)),
                ('Ob_N_V', models.CharField(max_length=200)),
                ('Corr_N_V', models.CharField(max_length=200)),
                ('report_id', models.ForeignKey(to='Test_Reports.Soil_building')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Test_Report_Descriptions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Start_Date', models.DateField(verbose_name=b'Cube Dated')),
                ('Description', models.CharField(max_length=200)),
                ('Strength', models.CharField(max_length=20)),
                ('mix', models.CharField(max_length=200, null=True, blank=True)),
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
                ('mix', models.BooleanField(default=False)),
                ('Address', models.CharField(max_length=200)),
                ('City', models.CharField(max_length=200)),
                ('Subject', models.CharField(max_length=200)),
                ('Refernce_no', models.CharField(max_length=200)),
                ('Refernce_Date', models.DateField(verbose_name=b'Letter Date')),
                ('Testing_Date', models.DateField(verbose_name=b'Date of Testing')),
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
