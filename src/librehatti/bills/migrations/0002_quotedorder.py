# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('useraccounts', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuotedOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quote_buyer_id', models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field='id')),
                ('quote_is_debit', models.BooleanField()),
                ('quote_delivery_address', models.ForeignKey(to='useraccounts.Address', to_field='id')),
                ('quote_organisation', models.ForeignKey(to='useraccounts.AdminOrganisations', to_field='id')),
                ('quote_date_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
