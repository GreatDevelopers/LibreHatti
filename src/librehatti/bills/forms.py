from django import forms
from librehatti.bills.models import *
from librehatti.catalog.models import ModeOfPayment,Category,Product
from librehatti.catalog.models import PurchaseOrder
import itertools
from ajax_select import make_ajax_field

from librehatti.config import _PARENT_CATEGORY
from librehatti.config import _SUB_CATEGORY
from librehatti.config import _ITEM

class BuyerForm(forms.ModelForm):
    buyer = make_ajax_field(QuotedOrder, 'buyer', 'buyer')

    class Meta:
        model = QuotedOrder
        exclude = ('is_active',)

    class Media:
        js = (
            'js/hide_add_buyer.js',
            'http://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js',
            'js/cheque_dd_date.js',
            )


"""
This form lets user to select item after categories are filtered in dropdown.
"""
class ItemSelectForm(forms.ModelForm):
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js',
            'js/quote_ajax.js',
        )

    try:
        parent_category = forms.ModelChoiceField(queryset=Category.objects.\
            filter(parent__parent__isnull=True).filter(parent__isnull=False), \
            label= _PARENT_CATEGORY)
        sub_category = forms.ModelChoiceField(queryset = Category.objects.all(),\
            label = _SUB_CATEGORY)
    except:
        pass

    item = forms.ModelChoiceField(queryset = Product.objects.all(), label = _ITEM)

    def __init__(self, *args, **kwargs):
         super(ItemSelectForm, self).__init__(*args, **kwargs)
         self.fields['parent_category'].widget.attrs={'class': 'parent_category'}
         self.fields['sub_category'].widget.attrs={'class': 'sub_category'}
         self.fields['item'].widget.attrs={'class': 'item'}


class SelectNoteForm(forms.Form):
    quoted_order = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    note_line = forms.ModelMultipleChoiceField(widget=forms.\
        CheckboxSelectMultiple(attrs={'class': 'note_checkbox'}),\
        queryset=NoteLine.objects.filter(is_permanent=0))