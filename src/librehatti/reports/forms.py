from django import forms

from search_choices import CLIENT_FIELD_CHOICES
from search_choices import CLIENT_ORDER_CHOICES
from search_choices import CONSTRAINT_CHOICES
from search_choices import MONTH_CHOICES

import datetime

import itertools

from librehatti.voucher.models import FinancialSession

from librehatti.catalog.models import ModeOfPayment
from librehatti.catalog.models import Surcharge


""" 
displays form for register
"""
class DailyReportForm(forms.Form):
    required_css_class = 'required'
    error_css_class = 'error'

    start_date = forms.DateField()
    end_date = forms.DateField()
    Type = forms.ModelChoiceField(queryset= ModeOfPayment.objects.all())


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
    
    additional_constraints = forms.MultipleChoiceField(required=False,
    widget=forms.CheckboxSelectMultiple, choices= CONSTRAINT_CHOICES)
    
    amount_greater_than = forms.FloatField(required=False, initial = 0)
    amount_less_than = forms.FloatField(required=False, initial = 1000000)

    start_date = forms.DateField(required=False, initial=str(datetime.date.\
        today().year) + '-04-01')
    end_date = forms.DateField(required=False, initial= datetime.date.today())
    year = forms.ChoiceField(choices= [(datetime.date.today().year, datetime.\
        date.today().year)] + [(x, x) for x in range(2000, 2050)], \
        required=False)
    month = forms.ChoiceField(MONTH_CHOICES)
    
    session_id = FinancialSession.objects.values_list('id',flat = True)
    session_start = FinancialSession.objects.values_list('session_start_date',\
        flat = True)
    session_end = FinancialSession.objects.values_list('session_end_date', \
        flat = True)
    session_choices = [('', '--------')] + [(id, str(start) + '-To-' + \
        str(end)) for id, start, end in itertools.izip(session_id, \
        session_start, session_end)]
    session = forms.ChoiceField(session_choices)
    
    surcharges = forms.ModelMultipleChoiceField(required=False,
    widget=forms.CheckboxSelectMultiple, queryset= Surcharge.objects.filter(
        taxes_included = True))
    paid_surcharges = forms.BooleanField()

    mode_of_payment_id = ModeOfPayment.objects.values_list('id', flat = True)
    mode = ModeOfPayment.objects.values_list('method', flat = True)
    mode_choices = [('', '--------')] + [(id, mode) for id, mode in itertools.\
        izip(mode_of_payment_id, mode)]
    mode_of_payment = forms.ChoiceField(mode_choices)

    grand_total = forms.BooleanField()
    all_registered_user = forms.BooleanField()