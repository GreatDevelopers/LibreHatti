# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-10 16:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('suspense', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LetterData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('street_address', models.CharField(max_length=500)),
                ('district', models.CharField(max_length=500)),
                ('pin', models.CharField(blank=True, max_length=10, null=True)),
                ('province', models.CharField(max_length=500)),
                ('contact_person', models.CharField(max_length=200)),
                ('contact_number', models.IntegerField()),
                ('letter_subject', models.CharField(max_length=500)),
                ('letter_date', models.DateField(auto_now_add=True)),
                ('site', models.CharField(max_length=500)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='StaffInTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='suspense.Staff')),
            ],
        ),
        migrations.CreateModel(
            name='TeamName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=500)),
            ],
        ),
        migrations.AddField(
            model_name='staffinteam',
            name='team_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='programmeletter.TeamName'),
        ),
        migrations.AddField(
            model_name='letterdata',
            name='team_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='programmeletter.TeamName'),
        ),
        migrations.AddField(
            model_name='letterdata',
            name='vehicle',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='suspense.Vehicle'),
        ),
    ]