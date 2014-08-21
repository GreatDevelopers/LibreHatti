from django import forms
from librehatti.bills.models import *


class ConfirmForm(forms.Form):
    quote_item = forms.CharField()
    quote_qty = forms.IntegerField()
    discount = forms.IntegerField()

