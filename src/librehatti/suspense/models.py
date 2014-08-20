from django.db import models
import datetime
from librehatti import catalog

class SuspenseOrder(models.Model):
    purchase_order = models.ForeignKey('catalog.PurchaseOrder')
    distance = models.IntegerField(default=0)
    is_cleared = models.BooleanField(default=False)
    def __unicode__(self):
        return '%s' % (self.id)

class SuspenseClearance(models.Model):
    suspense_id = models.IntegerField()
    work_charge =models.IntegerField(blank=True, null=True)
    labour_charge = models.IntegerField(blank=True, null=True)
    car_taxi_charge = models.IntegerField(blank=True, null=True)
    boring_charge_external = models.IntegerField(blank=True, null=True)
    boring_charge_internal = models.IntegerField(blank=True, null=True)
    lab_testing_staff = models.CharField(max_length=200)
    field_testing_staff = models.CharField(max_length=200)
    test_date = models.DateField(default=datetime.date.today)
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
    daily_income = models.IntegerField(blank=True)
    position = models.CharField(max_length=100)
    #lab = models.ForeignKey(Lab)
    email =models.EmailField(blank=True)
    def __unicode__(self):
        return self.name

class TaDa(models.Model):
    suspense = models.IntegerField()
    departure_time_from_tcc= models.TimeField()
    arrival_time_at_site = models.TimeField()
    departure_time_from_site = models.TimeField()
    arrival_time_at_tcc = models.TimeField()
    tada_amount = models.IntegerField()
    start_test_date = models.DateField()
    end_test_date = models.DateField()
    source_site = models.CharField(max_length=100)
    testing_site= models.CharField(max_length=100)
    testing_staff = models.CharField(max_length=100)
    def __unicode__(self):
       return self.suspense
