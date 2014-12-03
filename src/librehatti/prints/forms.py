from django import forms
from librehatti.catalog.models import Category

import itertools

from librehatti.config import _PARENT_CATEGORY
from librehatti.config import _SUB_CATEGORY


"""
This form lets the user select the category to generate the lab report.
"""
class LabReportForm(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()
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
