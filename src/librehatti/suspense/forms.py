from django.forms import ModelForm, TextInput
from models import SuspenseClearance
from models import TaDa
from models import Staff
from models import SuspenseOrder
from models import QuotedSuspenseOrder
from librehatti.catalog.models import Category
from django import forms
from librehatti.suspense.models import FinancialSession
from librehatti.suspense.models import VoucherId
from librehatti.suspense.models import Vehicle
import datetime

class Clearance_form(ModelForm):
    required_css_class = 'required'
    error_css_class = 'error'
    class Meta:
        model = SuspenseClearance
        exclude = []
    
    voucher_no = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    car_taxi_charge = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))


class SuspenseForm(ModelForm):
    required_css_class = 'required'
    error_css_class = 'error'
    class Meta:
        model = SuspenseOrder
        exclude = ('is_cleared',)

class QuotedSuspenseForm(ModelForm):
    class Meta:
        model = QuotedSuspenseOrder
        exclude = ('is_cleared',)

class TaDaSearch(forms.Form):
    ref_no = forms.ModelChoiceField(queryset= SuspenseOrder.objects.all())

class TaDaForm(ModelForm):
    required_css_class = 'required'
    error_css_class = 'error'
    class Meta:
        model = TaDa
        exclude = ('date_of_generation',)

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        exclude = []

    try:
        lab = forms.ModelChoiceField(queryset=Category.objects.\
        filter(parent__isnull=True))
    except:
        pass

class SessionSelectForm(forms.Form):
    session = forms.ModelChoiceField(queryset=FinancialSession.objects.all())
    voucher = forms.CharField()

class TransportForm1(forms.Form):
    required_css_class = 'required'
    error_css_class = 'error'
    Vehicle = forms.ModelChoiceField(queryset=Vehicle.objects.all())
    Date_of_generation = forms.DateField(initial = datetime.date.today)
    kilometer = forms.CharField()
    date = forms.DateField()