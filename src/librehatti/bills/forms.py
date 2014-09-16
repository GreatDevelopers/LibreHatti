from django import forms
from librehatti.bills.models import *
from librehatti.catalog.models import ModeOfPayment,Category,Product
import itertools

class ConfirmForm(forms.Form):
    item = forms.CharField()
    qty = forms.IntegerField()
    discount = forms.IntegerField()
    mode_of_payment = forms.ModelChoiceField(queryset=ModeOfPayment.objects.all())

"""
This form lets user to select item after categories are filtered in dropdown.
"""
class ItemSelectForm(forms.ModelForm):
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js',
            'js/ajax_quotation.js', 
        )

    try:
        parent_category = forms.ModelChoiceField(queryset=Category.objects.\
     	    filter(parent__parent__isnull=True).filter(parent__isnull=False))
     
        sub_category_id = Category.objects.values_list('id',flat=True)
        sub_category_name = Category.objects.values_list('name',flat=True)
        sub_category_choices = [('', '--------')] + [(id, name) for id, name in itertools.\
        izip(sub_category_id, sub_category_name)]
        sub_category = forms.ChoiceField(sub_category_choices)
	
    except:
        pass
    
    item = forms.ModelChoiceField(queryset = Product.objects.all())
    qty = forms.IntegerField() 
    def __init__(self, *args, **kwargs):
         super(ItemSelectForm, self).__init__(*args, **kwargs)
         self.fields['parent_category'].widget.attrs={'class': 'parent_category'}
         self.fields['sub_category'].widget.attrs={'class': 'sub_category'}
         self.fields['item'].widget.attrs={'class': 'item'}
         self.fields['qty'].widget.attrs={'class': 'qty'}

