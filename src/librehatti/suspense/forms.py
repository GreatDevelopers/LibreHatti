from django.forms import ModelForm, TextInput
from models import SuspenseClearance
from models import TaDa
from models import Staff
from models import SuspenseOrder
from models import QuotedSuspenseOrder
from librehatti.catalog.models import Category
from django import forms


class Clearance_form(ModelForm):
    class Meta:
        model = SuspenseClearance
        fields = ['work_charge','labour_charge','car_taxi_charge',
                  'boring_charge_external','boring_charge_internal',
		  'lab_testing_staff','field_testing_staff','test_date']


class SuspenseForm(ModelForm):
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
    class Meta:
        model = TaDa
        exclude = ('',)

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff

    try:
        lab = forms.ModelChoiceField(queryset=Category.objects.\
        filter(parent__isnull=True))
    except:
        pass