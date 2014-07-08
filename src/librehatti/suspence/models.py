from django.db import models

# Create your models here.
class TaDa(models.Model):
    #suspence = Model.ForeignKey(SuspenceOrder)
    departure_time_from_tcc= Model.TimeField()
    arrival_time_at_site = Model.TimeField()
    departure_time_from_tcc = Model.TimeField()
    arrival_time_at_tcc = Model.TimeField()
    tada_amount = Model.IntegerField(initial=0)
    start_test_date = Model.DateField()
    end_test_date = Model.DateField()
    testing_site= Model.CharField(max_length=100)
    testing_staff = Model.CharField(max_length=100)
    def __unicode__(self):
		return self.suspence


		
 
    
    
