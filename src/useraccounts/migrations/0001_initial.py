# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('street_address', models.CharField(max_length=100)),
                ('district', models.CharField(max_length=100)),
                ('pin', models.CharField(max_length=10, null=True, blank=True)),
                ('province', models.CharField(max_length=100)),
                ('nationality', models.CharField(default=b'India', max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Addresses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AdminOrganisations',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('telephone', models.CharField(max_length=500)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('fax', models.CharField(max_length=100, null=True, blank=True)),
                ('pan_no', models.CharField(max_length=100, null=True, blank=True)),
                ('stc_no', models.CharField(max_length=100, null=True, blank=True)),
                ('avatar', models.CharField(max_length=100, null=True, blank=True)),
                ('tagline', models.CharField(max_length=140, null=True, blank=True)),
                ('title', models.CharField(max_length=200)),
                ('address', models.ForeignKey(to='useraccounts.Address')),
            ],
            options={
                'verbose_name_plural': 'Admin Organisations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('telephone', models.CharField(max_length=500)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('fax', models.CharField(max_length=100, null=True, blank=True)),
                ('pan_no', models.CharField(max_length=100, null=True, blank=True)),
                ('stc_no', models.CharField(max_length=100, null=True, blank=True)),
                ('avatar', models.CharField(max_length=100, null=True, blank=True)),
                ('tagline', models.CharField(max_length=140, null=True, blank=True)),
                ('title', models.CharField(max_length=200, null=True, blank=True)),
                ('is_org', models.BooleanField(default=False)),
                ('company', models.CharField(max_length=200, null=True, blank=True)),
                ('address', models.ForeignKey(to='useraccounts.Address')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrganisationType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type_desc', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='customer',
            name='org_type',
            field=models.ForeignKey(to='useraccounts.OrganisationType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='adminorganisations',
            name='organisation_type',
            field=models.ForeignKey(to='useraccounts.OrganisationType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='adminorganisations',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
