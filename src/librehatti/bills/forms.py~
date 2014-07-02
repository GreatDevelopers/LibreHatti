from django import forms
from librehatti.bills.models import *

#class ConfirmForm(forms.Form):
    #quote_item = forms.CharField()
    #quote_qty = forms.IntegerField()


class ConfirmForm(ModelForm):
     class Meta:
         model = QuotedItem
         fields = ('quote_item', 'quote_qty')
