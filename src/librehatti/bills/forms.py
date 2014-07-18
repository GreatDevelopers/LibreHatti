from django import forms
from librehatti.bills.models import QuotedItem

#class ConfirmForm(ModelForm):
    #class Meta:
         #model = QuotedItem
         #fields = ['quote_item', 'quote_qty']


class ConfirmForm(forms.Form):
    quote_item = forms.CharField()
    quote_qty = forms.IntegerField()
    discount = forms.IntegerField()
