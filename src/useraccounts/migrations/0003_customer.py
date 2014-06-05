from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        (b'useraccounts', b'0002_admin_organisations'),
    ]

    operations = [
        migrations.CreateModel(
            name=b'customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, 
                auto_created=True, primary_key=True)),
                (b'user', models.OneToOneField(to=settings.AUTH_USER_MODEL, 
                to_field='id')),
                (b'address', models.ForeignKey(to=b'useraccounts.address', 
                to_field='id')),
                (b'telephone', models.CharField(max_length=500)),
                (b'date_joined', models.DateTimeField(auto_now_add=True)),
                (b'fax', models.CharField(max_length=100)),
                (b'avatar', models.CharField(max_length=100, null=True, 
                blank=True)),
                (b'tagline', models.CharField(max_length=140)),
                (b'title', models.CharField(max_length=200, null=True, 
                blank=True)),
                (b'is_org', models.BooleanField()),
                (b'org_type', models.ForeignKey(
                to=b'useraccounts.organisation_type', to_field='id')),
                (b'company', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
