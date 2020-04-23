from django.forms import ModelForm, TextInput
from . import models

# from librehatti.suspense.models import SuspenseClearance
from .models import SuspenseClearance
from .models import TaDa
from .models import Staff
from .models import SuspenseOrder
from .models import QuotedSuspenseOrder
from .models import CarTaxiAdvance

from librehatti.catalog.models import Category

from django import forms

from librehatti.suspense.models import FinancialSession
from librehatti.suspense.models import VoucherId
from librehatti.suspense.models import Vehicle

import datetime


class Clearance_form(ModelForm):
    """
    Form for clearance of order.
    """

    required_css_class = "required"
    error_css_class = "error"

    class Meta:
        model = SuspenseClearance
        exclude = ("work_charge",)
        widgets = {"session": forms.HiddenInput(), "voucher_no": forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(Clearance_form, self).__init__(*args, **kwargs)
        self.fields["voucher_no"].widget.attrs = {"class": "form-control"}
        self.fields["car_taxi_charge"].widget.attrs = {"class": "form-control"}
        self.fields["labour_charge"].widget.attrs = {"class": "form-control"}
        self.fields["boring_charge_external"].widget.attrs = {"class": "form-control"}
        self.fields["boring_charge_internal"].widget.attrs = {"class": "form-control"}
        self.fields["lab_testing_staff"].widget.attrs = {"class": "form-control"}
        self.fields["field_testing_staff"].widget.attrs = {"class": "form-control"}
        self.fields["test_date"].widget.attrs = {"class": "form-control"}
        self.fields["clear_date"].widget.attrs = {"class": "form-control"}
        self.fields["session"].widget.attrs = {"class": "form-control"}


class SuspenseForm(ModelForm):
    required_css_class = "required"
    error_css_class = "error"

    class Meta:
        model = SuspenseOrder
        exclude = ("is_cleared",)


class QuotedSuspenseForm(ModelForm):
    class Meta:
        model = QuotedSuspenseOrder
        exclude = ("is_cleared",)


class TaDaSearch(forms.Form):
    """
    Form for TaDa search.
    """

    ref_no = forms.ModelChoiceField(queryset=SuspenseOrder.objects.all())


class TaDaForm(ModelForm):
    """
    Transport and dialy allowance form.
    """

    required_css_class = "required"
    error_css_class = "error"

    class Meta:
        model = TaDa
        exclude = ("date_of_generation", "tada_amount", "tada_amount_without_tax")
        widgets = {"session": forms.HiddenInput(), "voucher_no": forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(TaDaForm, self).__init__(*args, **kwargs)
        self.fields["voucher_no"].widget.attrs = {"class": "form-control"}
        self.fields["session"].widget.attrs = {"class": "form-control"}
        self.fields["departure_time_from_tcc"].widget.attrs = {"class": "form-control"}
        self.fields["arrival_time_at_site"].widget.attrs = {"class": "form-control"}
        self.fields["departure_time_from_site"].widget.attrs = {"class": "form-control"}
        self.fields["arrival_time_at_tcc"].widget.attrs = {"class": "form-control"}
        self.fields["start_test_date"].widget.attrs = {"class": "form-control"}
        self.fields["end_test_date"].widget.attrs = {"class": "form-control"}
        self.fields["source_site"].widget.attrs = {"class": "form-control"}
        self.fields["testing_site"].widget.attrs = {"class": "form-control"}
        self.fields["testing_staff"].widget.attrs = {"class": "form-control"}


class StaffForm(forms.ModelForm):
    """
    Form for adding staff.
    """

    class Meta:
        model = Staff
        exclude = []

    try:
        lab = forms.ModelChoiceField(
            queryset=Category.objects.filter(parent__isnull=True)
        )
    except:
        pass


class SessionSelectForm(forms.Form):
    """
    Form for selection of sessions.
    """

    required_css_class = "required"
    error_css_class = "error"

    session = forms.ModelChoiceField(queryset=FinancialSession.objects.all())
    voucher = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(SessionSelectForm, self).__init__(*args, **kwargs)
        self.fields["voucher"].widget.attrs = {"class": "form-control"}
        self.fields["session"].widget.attrs = {
            "class": "btn btn-default dropdown-toggle"
        }


class TransportForm1(forms.Form):
    """
    Transport form.
    """

    required_css_class = "required"
    error_css_class = "error"
    Vehicle = forms.ModelChoiceField(queryset=Vehicle.objects.all())
    Date_of_generation = forms.DateField(initial=datetime.date.today)
    kilometer = forms.CharField()
    date = forms.DateField(label="Date of visit")

    def __init__(self, *args, **kwargs):
        super(TransportForm1, self).__init__(*args, **kwargs)
        self.fields["Date_of_generation"].widget.attrs = {"class": "form-control"}
        self.fields["kilometer"].widget.attrs = {"class": "form-control"}
        self.fields["date"].widget.attrs = {"class": "form-control"}
        self.fields["Vehicle"].widget.attrs = {
            "class": "btn btn-default dropdown-toggle"
        }


class CarTaxiAdvance_form(ModelForm):
    """
    Form for clearance of order.
    """

    required_css_class = "required"
    error_css_class = "error"

    class Meta:
        model = CarTaxiAdvance
        exclude = ("balance",)
        widgets = {"session": forms.HiddenInput(), "voucher_no": forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(CarTaxiAdvance_form, self).__init__(*args, **kwargs)
        self.fields["spent"].widget.attrs = {"class": "form-control"}
        self.fields["advance"].widget.attrs = {"class": "form-control"}
        self.fields["receipt_no"].widget.attrs = {"class": "form-control"}
        self.fields["receipt_session"].widget.attrs = {"class": "form-control"}
        self.fields["receipt_session"] = forms.ChoiceField(
            (o.id, str(o)) for o in FinancialSession.objects.all()
        )
