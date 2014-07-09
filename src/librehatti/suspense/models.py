from django.db import models

# Create your models here.
class SuspenseClearance(models.Model):

    #suspense_id = models.ForeignKey('SuspenseOrder')
    work_charge =models.IntegerField(blank=True, null=True)
    labour_charge = models.IntegerField(blank=True, null=True)
    car_taxi_charge = models.IntegerField(blank=True, null=True)
    boring_charge_external = models.IntegerField(blank=True, null=True)
    boring_charge_internal = models.IntegerField(blank=True, null=True)
    lab_testing_staff = models.CharField(max_length=200)
    field_testing_staff = models.CharField(max_length=200)
    Test_date = models.DateTimeField(auto_now_add=True)
    Clear_date = models.DateTimeField(auto_now_add=True)
