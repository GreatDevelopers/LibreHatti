from django import forms
from librehatti.bills.models import *


class ConfirmForm(forms.Form):
    quote_item = forms.CharField()
    quote_qty = forms.IntegerField()
    discount = forms.IntegerField()



class TransportForm1(forms.Form):
    vehicle_id = forms.CharField(max_length=20)
    job_id = forms.IntegerField()
    kilometer = forms.IntegerField()
    rate = forms.IntegerField(initial=10)  
    date = forms.DateField()


class TransportForm2(forms.Form):    
    kilometer = forms.IntegerField()
    date = forms.DateField()  
