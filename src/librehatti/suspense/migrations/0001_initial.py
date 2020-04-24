# -*- coding: utf-8 -*-
# Generated by Django 3.0.4 on 2020-03-16 17:30

import datetime

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [("catalog", "__first__"), ("bills", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Department",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=50)),
                ("address", models.CharField(max_length=150)),
                ("phone", models.CharField(blank=True, max_length=20)),
                ("dean", models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="StaffPosition",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("position", models.CharField(max_length=50)),
                ("rank", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="TaDa",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "date_of_generation",
                    models.DateField(default=datetime.date.today),
                ),
                ("voucher_no", models.IntegerField()),
                ("session", models.IntegerField()),
                ("departure_time_from_tcc", models.TimeField()),
                ("arrival_time_at_site", models.TimeField()),
                ("departure_time_from_site", models.TimeField()),
                ("arrival_time_at_tcc", models.TimeField()),
                ("tada_amount", models.IntegerField()),
                ("tada_amount_without_tax", models.IntegerField()),
                ("start_test_date", models.DateField()),
                ("end_test_date", models.DateField()),
                (
                    "source_site",
                    models.CharField(default="GNDEC, Ludhiana", max_length=100),
                ),
                ("testing_site", models.CharField(max_length=100)),
                ("testing_staff", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Transport",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("kilometer", models.CharField(max_length=500)),
                ("rate", models.FloatField(default=10.0)),
                ("date_of_generation", models.DateField()),
                ("date", models.CharField(blank=True, max_length=600)),
                ("total", models.IntegerField()),
                ("voucher_no", models.IntegerField()),
                (
                    "session",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="catalog.FinancialSession",
                    ),
                ),
            ],
            options={"verbose_name_plural": "Transport"},
        ),
        migrations.CreateModel(
            name="Vehicle",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("vehicle_id", models.CharField(max_length=20)),
                ("vehicle_no", models.CharField(max_length=20)),
                ("vehicle_name", models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name="TransportBillOfSession",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("transportbillofsession", models.IntegerField()),
                (
                    "session",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="catalog.FinancialSession",
                    ),
                ),
                (
                    "transport",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="suspense.Transport",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="transport",
            name="vehicle",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="suspense.Vehicle",
            ),
        ),
        migrations.CreateModel(
            name="TaDa_Tax_Detail",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("amount", models.IntegerField()),
                (
                    "tada",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="suspense.TaDa",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SuspenseOrder",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("voucher", models.IntegerField()),
                ("distance_estimated", models.IntegerField(default=0)),
                ("is_cleared", models.BooleanField(default=False)),
                (
                    "purchase_order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="catalog.PurchaseOrder",
                    ),
                ),
                (
                    "session_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="catalog.FinancialSession",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SuspenseClearedRegister",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("suspenseclearednumber", models.IntegerField()),
                ("voucher_no", models.IntegerField()),
                (
                    "session",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="catalog.FinancialSession",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SuspenseClearance",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("voucher_no", models.IntegerField()),
                ("work_charge", models.IntegerField(blank=True, null=True)),
                ("labour_charge", models.IntegerField(blank=True, null=True)),
                ("car_taxi_charge", models.IntegerField(blank=True, null=True)),
                (
                    "boring_charge_external",
                    models.IntegerField(blank=True, null=True),
                ),
                (
                    "boring_charge_internal",
                    models.IntegerField(blank=True, null=True),
                ),
                (
                    "lab_testing_staff",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "field_testing_staff",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "test_date",
                    models.CharField(blank=True, max_length=600, null=True),
                ),
                ("clear_date", models.DateField()),
                (
                    "session",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="catalog.FinancialSession",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Staff",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(max_length=5)),
                ("name", models.CharField(max_length=50)),
                ("daily_ta_da", models.IntegerField(blank=True)),
                ("seniority_credits", models.IntegerField()),
                ("always_included", models.BooleanField(default=True)),
                ("email", models.EmailField(blank=True, max_length=254)),
                (
                    "department",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="suspense.Department",
                    ),
                ),
                (
                    "lab",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="catalog.Category",
                    ),
                ),
                (
                    "position",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="suspense.StaffPosition",
                    ),
                ),
            ],
            options={"verbose_name_plural": "Staff"},
        ),
        migrations.CreateModel(
            name="QuotedSuspenseOrder",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("distance_estimated", models.IntegerField(default=0)),
                ("is_cleared", models.BooleanField(default=False)),
                (
                    "quoted_order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bills.QuotedOrder",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CarTaxiAdvance",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("voucher_no", models.IntegerField()),
                ("spent", models.IntegerField()),
                ("advance", models.IntegerField()),
                ("balance", models.IntegerField()),
                ("receipt_no", models.IntegerField()),
                ("receipt_session", models.IntegerField()),
                (
                    "session",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="catalog.FinancialSession",
                    ),
                ),
            ],
        ),
    ]