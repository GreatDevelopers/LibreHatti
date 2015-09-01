"""
Forms of programmeletter are ..
"""
from django import forms

from librehatti.programmeletter.models import *
from librehatti.programmeletter.models import StaffInTeam

from librehatti.catalog.models import Category

from librehatti.suspense.models import Staff

from ajax_select import make_ajax_field


class StaffInTeamForm(forms.ModelForm):
    """
    Form for selecting staff for team.
    """
    # staff = forms.ModelChoiceField(queryset=Staff.objects.all())
    staff = make_ajax_field(StaffInTeam, 'staff', 'staff')

    def __init__(self, *args, **kwargs):
         super(StaffInTeamForm, self).__init__(*args, **kwargs)
         self.fields['staff'].widget.attrs={'class':'form-control'}


class TeamNameForm(forms.ModelForm):
    team_name = forms.CharField()
    def __init__(self, *args, **kwargs):
         super(TeamNameForm, self).__init__(*args, **kwargs)
         self.fields['team_name'].widget.attrs={'class':'form-control'}

class LetterDataForm(forms.ModelForm):
    buyer = make_ajax_field(LetterData  , 'buyer', 'buyer')
    class Meta:
        model = LetterData
        exclude = ['']
    
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js',
            'js/ajax.js',
            'js/price_per_unit.js',
            )
