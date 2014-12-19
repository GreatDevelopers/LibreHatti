from django.db import models
import datetime

from librehatti.voucher.models import VoucherId
from librehatti.voucher.models import FinancialSession

from librehatti.bills.models import QuotedOrder

from librehatti.catalog.models import PurchaseOrder, Category

import simplejson


class SuspenseOrder(models.Model):
    voucher = models.IntegerField()
    purchase_order = models.ForeignKey(PurchaseOrder)
    session_id = models.ForeignKey(FinancialSession)
    distance_estimated = models.IntegerField(default=0)
    is_cleared = models.BooleanField(default=False)
    def __unicode__(self):
        return '%s' % (self.id)


class SuspenseClearance(models.Model):
    session = models.ForeignKey(FinancialSession)
    voucher_no = models.IntegerField()
    work_charge =models.IntegerField(blank=True, null=True)
    labour_charge = models.IntegerField(blank=True, null=True)
    car_taxi_charge = models.IntegerField(blank=True, null=True)
    boring_charge_external = models.IntegerField(blank=True, null=True)
    boring_charge_internal = models.IntegerField(blank=True, null=True)
    lab_testing_staff = models.CharField(max_length=200)
    field_testing_staff = models.CharField(max_length=200)
    test_date = models.CharField(max_length=600)
    clear_date = models.DateField(default=datetime.date.today)


class Department(models.Model):
    title = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, blank=True)
    dean = models.CharField(max_length=50, blank=True)
    def __unicode__(self):
        return self.title


class Staff(models.Model):
    department = models.ForeignKey(Department)
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=50)
    daily_ta_da = models.IntegerField(blank=True)
    position = models.CharField(max_length=100)
    lab = models.ForeignKey(Category)
    email =models.EmailField(blank=True)

    class Meta:
        verbose_name_plural = "Staff"

    def __unicode__(self):
        return self.name


class TaDa(models.Model):
    date_of_generation = models.DateField(default=datetime.date.today)
    voucher_no = models.IntegerField()
    session = models.IntegerField()
    departure_time_from_tcc= models.TimeField()
    arrival_time_at_site = models.TimeField()
    departure_time_from_site = models.TimeField()
    arrival_time_at_tcc = models.TimeField()
    tada_amount = models.IntegerField()
    start_test_date = models.DateField()
    end_test_date = models.DateField()
    source_site = models.CharField(max_length=100, default = 'GNDEC, Ludhiana')
    testing_site= models.CharField(max_length=100)
    testing_staff = models.CharField(max_length=100)
    def __unicode__(self):
       return self.suspense


class QuotedSuspenseOrder(models.Model):
    quoted_order = models.ForeignKey('bills.QuotedOrder')
    distance_estimated = models.IntegerField(default=0)
    is_cleared = models.BooleanField(default=False)
    def __unicode__(self):
        return '%s' % (self.id)


class Vehicle(models.Model):
    vehicle_id = models.CharField(max_length=20)
    vehicle_no = models.CharField(max_length=20)
    vehicle_name = models.CharField(max_length=20)
    def __unicode__(self):
        return '%s' % (self.vehicle_no)


class Transport(models.Model):
    vehicle = models.ForeignKey(Vehicle)
    kilometer = models.CharField(max_length=500)
    rate = models.FloatField(default=10.0)
    date_of_generation = models.DateField()
    date = models.CharField(blank=True, max_length=600)
    total = models.IntegerField()
    voucher_no = models.IntegerField()
    session = models.ForeignKey(FinancialSession)
    '''def save(self, *args, **kwargs):

        # Now decode the kilometers
        jsonkilometer = simplejson.loads(self.kilometer)
        total_km = 0;

        #calculate the total kms
        for km in jsonkilometer:
            total_km += float(km)

        # Now calculate the total and save it in model
        self.total = total_km * self.rate
        super(Transport, self).save(*args, **kwargs)
    '''

    class Meta:
        verbose_name_plural = "Transport"

    def __unicode__(self):
        return '%s' % (self.vehicle)