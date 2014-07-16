from django.db import models
from librehatti.catalog.models import PurchaseOrder


class SuspenseOrder(models.Model):
    purchase_order_id = models.IntegerField()
    transportation = models.IntegerField()
    
    

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


		
 
    
    
