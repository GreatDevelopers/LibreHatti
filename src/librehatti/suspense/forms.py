from django.forms import ModelForm
from models import SuspenseClearance
from librehatti.suspense.choices import CHOICES
from django import forms
# Create your forms here.
class Clearance_form(ModelForm):
    class Meta:
    	model = SuspenseClearance
    	fields = ['work_charge','labour_charge','car_taxi_charge','boring_charge_external','boring_charge_internal',
		  'lab_testing_staff','field_testing_staff','test_date']

class SuspenseForm(forms.Form):
        Purchase_order = forms.ChoiceField(choices=CHOICES)
        distance=forms.IntegerField()
      
