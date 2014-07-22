from django import forms
from search_choices import CLIENT_FIELD_CHOICES
from search_choices import CLIENT_ORDER_CHOICES
from search_choices import CONSTRAINT_CHOICES
import datetime


"""
displays checkboxes for Client Search
"""
class ClientForm(forms.Form):
    client_fields = forms.MultipleChoiceField(required=False,
    widget=forms.CheckboxSelectMultiple, choices=CLIENT_FIELD_CHOICES)


"""
displays chechboxes for Order Search
"""        
class OrderForm(forms.Form):
    order = forms.MultipleChoiceField(required=False,
    widget=forms.CheckboxSelectMultiple, choices=CLIENT_ORDER_CHOICES)


"""
displays checkboxes for Constraints
"""
class AddConstraints(forms.Form):
    start_date = forms.DateField(required=False, initial='2014-01-01')
    end_date = forms.DateField(required=False, initial= datetime.date.today())
    additional_constraints = forms.MultipleChoiceField(required=False,
    widget=forms.CheckboxSelectMultiple, choices= CONSTRAINT_CHOICES)
    amount_greater_than = forms.FloatField(required=False, initial = 0)
    amount_less_than = forms.FloatField(required=False, initial = 1000000)
