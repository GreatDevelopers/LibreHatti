from django import forms

from search_choices import CLIENT_FIELD_CHOICES
from search_choices import CLIENT_ORDER_CHOICES


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
