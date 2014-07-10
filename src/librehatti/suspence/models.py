from django.db import models

# Create your models here.
class TaDa(models.Model):
    #suspence = models.ForeignKey(SuspenceOrder)
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
   # def __unicode__(self):
	#	return self.suspence


		
 
    
    
