# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuotedItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quote_order', models.ForeignKey(to='catalog.PurchaseOrder', to_field='id')),
                ('quote_price', models.IntegerField()),
                ('quote_qty', models.IntegerField()),
                ('quote_discount', models.IntegerField()),
                ('quote_item', models.ForeignKey(to='catalog.Product', to_field='id')),
                ('status', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
