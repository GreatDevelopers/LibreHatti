from django import forms

from librehatti.Test_Reports.models import Test_Reports

from librehatti.bills.models import *

from librehatti.catalog.models import ModeOfPayment, Category, Product

from librehatti.catalog.models import PurchaseOrder

import itertools

from ajax_select import make_ajax_field

from librehatti.config import _PARENT_CATEGORY

from librehatti.config import _SUB_CATEGORY

from librehatti.config import _ITEM

from librehatti.config import _TYPE


class Test_Reports_Form(forms.ModelForm):


    class Meta:
	model = Test_Reports

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js',
            'js/Test_Reports.js',
             )

    
class Test_Reports_Des(forms.ModelForm):


    class Media:
        js = (
            'js/hide_add_buyer.js',
            'http://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js',
            'js/Test_Reports.js',
             )
    
    def __init__(self,  *args, **kwargs):
        super(Test_Reports_Des, self).__init__(*args, **kwargs)
        self.fields['Description'].widget.attrs = {'class':'description'}
        self.fields['Strength'].widget.attrs = {'class':'strength'}
        self.fields['mix'].widget.attrs = {'class':'mix'}

class Soil_building_Des(forms.ModelForm):


    class Media:
        js = (
            'js/hide_add_buyer.js',
            'http://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js',
            'js/Test_Reports.js',
             )
    
    def __init__(self,  *args, **kwargs):
        super(Soil_building_Des, self).__init__(*args, **kwargs)
        self.fields['Dt'].widget.attrs = {'class':'Dt'}
        self.fields['Ob_Pr'].widget.attrs = {'class':'Ob_Pr'}
        self.fields['Corr_F'].widget.attrs = {'class':'Corr_F'}
        self.fields['Ob_N_V'].widget.attrs = {'class':'Ob_N_V'}
        self.fields['Corr_N_V'].widget.attrs = {'class':'Corr_N_V'}

