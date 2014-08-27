from django import forms
from librehatti.catalog.models import Category

"""
This form lets the user select the category to generate the lab report.
"""
class LabReportForm(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()
    parent_category = forms.ModelChoiceField(queryset=Category.objects.\
    filter(parent__parent__isnull=True).filter(parent__isnull=False))
    sub_category = forms.ChoiceField()
