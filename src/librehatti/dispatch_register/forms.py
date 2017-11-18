"""
forms of dispatch_register are..
"""
from django import forms
from .models import DispatchEntry, SubjectsChoice, RemarksChoice
from ajax_select import make_ajax_field
from django.forms.widgets import CheckboxSelectMultiple

class DispatchForm(forms.ModelForm):
    """
    This form lets user to fill dispatch entry and enable user to
    select multiple subjects and remarks for a client.
    name_of_Dept_or_Client field is ajax field which means
    it will search for registered clients.
    """

    name_of_Dept_or_Client=make_ajax_field(DispatchEntry, \
    'name_of_Dept_or_Client', 'buyer')
    class Meta:
        model = DispatchEntry

    def __init__(self, *args, **kwargs):
        super(DispatchForm, self).__init__(*args, **kwargs)
        self.fields['agency'].required = False
        self.fields['subjects']=forms.ModelMultipleChoiceField\
        (queryset=SubjectsChoice.objects.all(), \
        widget=forms.CheckboxSelectMultiple)
        self.fields['remarks']=forms.ModelMultipleChoiceField\
        (queryset=RemarksChoice.objects.all(), \
        widget=forms.CheckboxSelectMultiple)

class SubjectsForm(forms.ModelForm):
    """
    This form lets user to add new subjects.
    """

    class Meta:
        model = SubjectsChoice

class RemarksForm(forms.ModelForm):
    """
    This form lets user to add new remarks.
    """

    class Meta:
        model = RemarksChoice
