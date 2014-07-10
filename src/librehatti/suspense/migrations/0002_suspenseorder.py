# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('suspense', '0001_initial'),
        ('catalog', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='SuspenseOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('purchase_order_id', models.ForeignKey(to='catalog.PurchaseOrder', to_field='id')),
                ('transportation', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
