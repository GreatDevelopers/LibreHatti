from django.db import models
import datetime

from librehatti.voucher.models import VoucherId
from librehatti.voucher.models import FinancialSession

from librehatti.bills.models import QuotedOrder

from librehatti.catalog.models import PurchaseOrder, Category

import simplejson

<<<<<<< HEAD

class SuspenseOrder(models.Model):
    voucher = models.IntegerField()
    purchase_order = models.ForeignKey(PurchaseOrder)
    session_id = models.ForeignKey(FinancialSession)
    distance_estimated = models.IntegerField()
=======


class SuspenseOrder(models.Model):
    voucher = models.IntegerField()
    purchase_order = models.ForeignKey(PurchaseOrder, verbose_name='_PURCHASE_ORDER')
    session_id = models.ForeignKey(FinancialSession)
    distance_estimated = models.IntegerField(verbose_name='_DISTANCE_ESTIMATED')
>>>>>>> upstream/dirty
    is_cleared = models.BooleanField(default=False)
    def __unicode__(self):
        return '%s' % (self.id)

class SuspenseClearance(models.Model):
    session = models.ForeignKey(FinancialSession)
    voucher_no = models.IntegerField()
<<<<<<< HEAD
    work_charge =models.IntegerField(blank=True, null=True)
    labour_charge = models.IntegerField(blank=True, null=True)
    car_taxi_charge = models.IntegerField(blank=True, null=True)
=======
    work_charge =models.IntegerField(blank=True, null=True, verbose_name='_WORK_CHARGE')
    labour_charge = models.IntegerField(blank=True, null=True)
    car_taxi_charge = models.IntegerField(blank=True, null=True, verbose_name='_CAR_TAXI_CHARGE')
>>>>>>> upstream/dirty
    boring_charge_external = models.IntegerField(blank=True, null=True)
    boring_charge_internal = models.IntegerField(blank=True, null=True)
    lab_testing_staff = models.CharField(max_length=200)
    field_testing_staff = models.CharField(max_length=200)
<<<<<<< HEAD
    test_date = models.DateField(default=datetime.date.today)
    clear_date = models.DateField(default=datetime.date.today)


class Department(models.Model):
    title = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, blank=True)
=======
    test_date = models.DateField(default=datetime.date.today, verbose_name='_TEST_DATE')
    clear_date = models.DateField(default=datetime.date.today, verbose_name='_CLEAR_DATE')


class Department(models.Model):
    title = models.CharField(max_length=50, verbose_name='_TITLE')
    address = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, blank=True, verbose_name='_PHONE')
>>>>>>> upstream/dirty
    dean = models.CharField(max_length=50, blank=True)
    def __unicode__(self):
        return self.title


class Staff(models.Model):
    department = models.ForeignKey(Department)
<<<<<<< HEAD
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=50)
    daily_ta_da = models.IntegerField(blank=True)
    position = models.CharField(max_length=100)
=======
    code = models.CharField(max_length=5, verbose_name='_CODE')
    name = models.CharField(max_length=50)
    daily_ta_da = models.IntegerField(blank=True)
    position = models.CharField(max_length=100, verbose_name='_POSITION')
>>>>>>> upstream/dirty
    lab = models.ForeignKey(Category)
    email =models.EmailField(blank=True)

    class Meta:
        verbose_name_plural = "Staff"

    def __unicode__(self):
        return self.name

class TaDa(models.Model):
    Date_of_generation = models.DateField(default = datetime.date.today)
    voucher_no = models.IntegerField()
    session = models.IntegerField()
    departure_time_from_tcc= models.TimeField()
    arrival_time_at_site = models.TimeField()
    departure_time_from_site = models.TimeField()
    arrival_time_at_tcc = models.TimeField()
<<<<<<< HEAD
    tada_amount = models.IntegerField()
=======
    tada_amount = models.IntegerField(verbose_name='_TADA_AMOUNT')
>>>>>>> upstream/dirty
    start_test_date = models.DateField()
    end_test_date = models.DateField()
    source_site = models.CharField(max_length=100)
    testing_site= models.CharField(max_length=100)
    testing_staff = models.CharField(max_length=100)
    def __unicode__(self):
       return self.suspense

class QuotedSuspenseOrder(models.Model):
    quote_order = models.ForeignKey('bills.QuotedOrder')
    distance = models.IntegerField(default=0)
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
    Date_of_generation = models.DateField()
    Date = models.CharField(blank=True,max_length=600)
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
