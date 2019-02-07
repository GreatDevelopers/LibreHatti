from django.db import models
import datetime

from librehatti.voucher.models import VoucherId
from librehatti.voucher.models import FinancialSession

from librehatti.bills.models import QuotedOrder

from librehatti.catalog.models import PurchaseOrder, Category

import simplejson


class SuspenseOrder(models.Model):
    """
    Stores order with over head costs.
    """
    voucher = models.IntegerField()
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE,)
    session_id = models.ForeignKey(FinancialSession, on_delete=models.CASCADE,)
    distance_estimated = models.IntegerField(default=0)
    is_cleared = models.BooleanField(default=False)
    def __str__(self):
        return '%s' % (self.id)


class SuspenseClearance(models.Model):
    """
    Stores clearance of suspense orders.
    """
    session = models.ForeignKey(FinancialSession, on_delete=models.CASCADE,)
    voucher_no = models.IntegerField()
    work_charge =models.IntegerField(blank=True, null=True)
    labour_charge = models.IntegerField(blank=True, null=True)
    car_taxi_charge = models.IntegerField(blank=True, null=True)
    boring_charge_external = models.IntegerField(blank=True, null=True)
    boring_charge_internal = models.IntegerField(blank=True, null=True)
    lab_testing_staff = models.CharField(max_length=200, blank=True, null=True)
    field_testing_staff = models.CharField(max_length=200,blank=True,null=True)
    test_date = models.CharField(max_length=600, blank=True, null=True)
    clear_date = models.DateField()


class Department(models.Model):
    """
    Stores department.
    """
    title = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, blank=True)
    dean = models.CharField(max_length=50, blank=True)
    def __str__(self):
        return self.title

class StaffPosition(models.Model):
    """
    Stores position of staff.
    """
    position = models.CharField(max_length=50)
    rank = models.IntegerField()

    def __str__(self):
        return self.position

class Staff(models.Model):
    """
    Stores staff and map it with position.
    """
    department = models.ForeignKey(Department, on_delete=models.CASCADE,)
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=50)
    daily_ta_da = models.IntegerField(blank=True)
    position = models.ForeignKey(StaffPosition, on_delete=models.CASCADE,)
    seniority_credits = models.IntegerField()
    always_included = models.BooleanField(default=True)
    lab = models.ForeignKey(Category, on_delete=models.CASCADE,)
    email =models.EmailField(blank=True)

    class Meta:
        verbose_name_plural = "Staff"

    def __str__(self):
        return self.name


class TaDa(models.Model):
    """
    Model to store transport and daily allowances.
    """
    date_of_generation = models.DateField(default=datetime.date.today)
    voucher_no = models.IntegerField()
    session = models.IntegerField()
    departure_time_from_tcc= models.TimeField()
    arrival_time_at_site = models.TimeField()
    departure_time_from_site = models.TimeField()
    arrival_time_at_tcc = models.TimeField()
    tada_amount = models.IntegerField()
    tada_amount_without_tax = models.IntegerField()
    start_test_date = models.DateField()
    end_test_date = models.DateField()
    source_site = models.CharField(max_length=100, default = 'GNDEC, Ludhiana')
    testing_site= models.CharField(max_length=100)
    testing_staff = models.CharField(max_length=100)
    def __str__(self):
       return self.suspense

class TaDa_Tax_Detail(models.Model):
    tada = models.ForeignKey(TaDa, on_delete=models.CASCADE,)
    name = models.CharField(max_length=100)
    amount = models.IntegerField()

class QuotedSuspenseOrder(models.Model):
    """
    Stores Quoted suspense order.
    """
    quoted_order = models.ForeignKey('bills.QuotedOrder', on_delete=models.CASCADE,)
    distance_estimated = models.IntegerField(default=0)
    is_cleared = models.BooleanField(default=False)
    def __str__(self):
        return '%s' % (self.id)


class Vehicle(models.Model):
    """
    Stores vehicle details.
    """
    vehicle_id = models.CharField(max_length=20)
    vehicle_no = models.CharField(max_length=20)
    vehicle_name = models.CharField(max_length=20)
    def __str__(self):
        return '%s' % (self.vehicle_no)


class Transport(models.Model):
    """
    Stores Transportation details.
    """
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE,)
    kilometer = models.CharField(max_length=500)
    rate = models.FloatField(default=10.0)
    date_of_generation = models.DateField()
    date = models.CharField(blank=True, max_length=600)
    total = models.IntegerField()
    voucher_no = models.IntegerField()
    session = models.ForeignKey(FinancialSession, on_delete=models.CASCADE,)
    '''def save(self, *args, **kwargs):

        # Now decode the kilometers
        jsonkilometer = simplejson.loads(self.kilometer)
        total_km = 0;

        # calculate the total kms
        for km in jsonkilometer:
            total_km += float(km)

        # Now calculate the total and save it in model
        self.total = total_km * self.rate
        super(Transport, self).save(*args, **kwargs)
    '''

    class Meta:
        verbose_name_plural = "Transport"

    def __str__(self):
        return '%s' % (self.vehicle)


class TransportBillOfSession(models.Model):
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE,)
    transportbillofsession = models.IntegerField()
    session = models.ForeignKey(FinancialSession, on_delete=models.CASCADE,)


class SuspenseClearedRegister(models.Model):
    suspenseclearednumber = models.IntegerField()
    voucher_no = models.IntegerField()
    session = models.ForeignKey(FinancialSession, on_delete=models.CASCADE,)


class CarTaxiAdvance(models.Model):
    voucher_no = models.IntegerField()
    session = models.ForeignKey(FinancialSession, on_delete=models.CASCADE,)
    spent = models.IntegerField()
    advance = models.IntegerField()
    balance = models.IntegerField()
    receipt_no = models.IntegerField()
    receipt_session = models.IntegerField()
