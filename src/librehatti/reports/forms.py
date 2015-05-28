from django import forms

from search_choices import CLIENT_FIELD_CHOICES
from search_choices import CLIENT_ORDER_CHOICES
from search_choices import CONSTRAINT_CHOICES
from search_choices import MONTH_CHOICES

from useraccounts.models import *

import datetime

import itertools

from librehatti.voucher.models import FinancialSession

from librehatti.catalog.models import Category

from librehatti.config import _PARENT_CATEGORY
from librehatti.config import _SUB_CATEGORY
from librehatti.config import _ORG_TYPE

from librehatti.catalog.models import ModeOfPayment
from librehatti.catalog.models import Surcharge


"""
A form for date range selection
"""
class DateRangeSelectionForm(forms.Form):
    required_css_class = 'required'
    error_css_class = 'error'

    start_date = forms.DateField()
    end_date = forms.DateField()
    def __init__(self, *args, **kwargs):
        super(DateRangeSelectionForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.attrs={'class':'form-control'}
        self.fields['end_date'].widget.attrs={'class':'form-control'}

"""
displays form for daily register report
"""
class DailyReportForm(forms.Form):
    required_css_class = 'required'
    error_css_class = 'error'

    mode_of_payment = forms.ChoiceField(choices=[('1','Cash'),('2','DD/Cheque/RTGS')])
    def __init__(self, *args, **kwargs):
        super(DailyReportForm, self).__init__(*args, **kwargs)
        self.fields['mode_of_payment'].widget.attrs={'class':'btn btn-default dropdown-toggle'}

'''
displays form for Consultancy Funds
'''
class ConsultancyFunds(forms.Form):
    required_css_class = 'required'
    error_css_class = 'error'

    parent_category = forms.ModelChoiceField(queryset=Category.objects.\
    filter(parent__parent__isnull=True).filter(parent__isnull=False),\
    label=_PARENT_CATEGORY)
    try:
        sub_category_id = Category.objects.values_list('id', flat=True)
        sub_category_name = Category.objects.values_list('name', flat=True)
        sub_category_choices = [('', '--------')] + [(id, name) for id,\
        name in itertools.izip(sub_category_id, sub_category_name)]
        sub_category = forms.ChoiceField(sub_category_choices,\
            label=_SUB_CATEGORY)
    except:
        pass
    def __init__(self, *args, **kwargs):
        super(ConsultancyFunds, self).__init__(*args, **kwargs)
        self.fields['parent_category'].widget.attrs={'class':'btn btn-default dropdown-toggle'}
        self.fields['sub_category'].widget.attrs={'class':'btn btn-default dropdown-toggle'}


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


class MonthYearForm(forms.Form):
    required_css_class = 'required'
    error_css_class = 'error'

    month = forms.ChoiceField(MONTH_CHOICES)
    year = forms.ChoiceField(choices= [(datetime.date.today().year, datetime.\
        date.today().year)] + [(x, x) for x in range(2000, 2050)], \
        required=False)
    def __init__(self, *args, **kwargs):
        super(MonthYearForm, self).__init__(*args, **kwargs)
        self.fields['month'].widget.attrs={'class':'form-control'}
        self.fields['year'].widget.attrs={'class':'form-control'}


class PaidTaxesForm(forms.Form):
    required_css_class = 'required'
    error_css_class = 'error'

    paid_service_tax = forms.IntegerField(initial=0)
    paid_education_tax = forms.IntegerField(initial=0)
    paid_higher_education_tax = forms.IntegerField(initial=0)
    def __init__(self, *args, **kwargs):
        super(PaidTaxesForm, self).__init__(*args, **kwargs)
        self.fields['paid_service_tax'].widget.attrs={'class':'form-control'}
        self.fields['paid_education_tax'].widget.attrs={'class':'form-control'}
        self.fields['paid_higher_education_tax'].widget.attrs={\
        'class':'form-control'}

class OrgType(forms.Form):
    required_css_class = 'required'
    error_css_class = 'error'

    parent_category = forms.ModelChoiceField(queryset=OrganisationType.objects. \
        all(),label=_ORG_TYPE)
    
    def __init__(self, *args, **kwargs):
        super(OrgType, self).__init__(*args, **kwargs)
        self.fields['parent_category'].widget.attrs={'class':'btn btn-default dropdown-toggle'}