"""
Forms of catalog are ..
"""
from django import forms

from librehatti.catalog.models import Category
from librehatti.catalog.models import Product
from librehatti.catalog.models import PurchasedItem
from librehatti.catalog.models import PurchaseOrder, ModeOfPayment
from librehatti.catalog.models import TaxesApplied
from librehatti.catalog.models import SpecialCategories

from librehatti.voucher.models import FinancialSession

import itertools

from ajax_select import make_ajax_field

from librehatti.config import _PARENT_CATEGORY
from librehatti.config import _SUB_CATEGORY
from librehatti.config import _ITEM
from librehatti.config import _TYPE


"""
This form allows user to fill the category name of product
"""
class AddCategory(forms.Form):
    """
    used by catalog views to specify name and different categories used.
    """
    category_name = forms.CharField(max_length=256)
    categories = forms.ModelChoiceField(queryset=Category.objects.all())


"""
This form lets user to select item after categories
are filtered in dropdown.
"""
class ItemSelectForm(forms.ModelForm):
    class Media:
        js = (
            'js/ajax.js',
            'js/price_per_unit.js'
        )

    try:
        parent_category = forms.ModelChoiceField(queryset=Category.objects.\
            filter(parent__parent__isnull=True).filter(parent__isnull=False), \
            label= _PARENT_CATEGORY)
        sub_category = forms.ModelChoiceField\
        (queryset = Category.objects.all(),label = _SUB_CATEGORY)
    except:
        pass

    item = forms.ModelChoiceField\
    (queryset = Product.objects.all(), label = _ITEM)
    CHOICES = (('', '---------',), ('1', 'Lab Work',), ('2', 'Field Work',),
        ('3', 'Other Services',))
    type = forms.ChoiceField(choices=CHOICES, label = _TYPE)
    price_per_unit = forms.IntegerField()

    def __init__(self, *args, **kwargs):
         super(ItemSelectForm, self).__init__(*args, **kwargs)
         self.fields['type'].widget.attrs={'class': 'type'}
         self.fields['parent_category'].widget.attrs={'class': 'parent_category'}
         self.fields['sub_category'].widget.attrs={'class': 'sub_category'}
         self.fields['item'].widget.attrs={'class': 'item'}
         self.fields['price_per_unit'].widget.attrs={'class': 'price_per_unit'}


class BuyerForm(forms.ModelForm):
    buyer = make_ajax_field(PurchaseOrder, 'buyer', 'buyer')

    class Meta:
        model = PurchaseOrder
        exclude = ('is_active',)

    class Media:
        js = (
            'js/hide_add_buyer.js',
            'js/cheque_dd_date.js',
            )


class ChangeRequestForm(forms.Form):
    session = forms.ModelChoiceField(queryset=FinancialSession.objects.all())
    purchase_order = forms.CharField(max_length=10)
    def __init__(self, *args, **kwargs):
       super(ChangeRequestForm, self).__init__(*args, **kwargs)
       self.fields['purchase_order'].widget.attrs={'class':'form-control'}
       self.fields['session'].widget.attrs={'class':'btn btn-default dropdown-toggle'}


class SpecialCategoriesForm(forms.ModelForm):

    class Meta:
        model = SpecialCategories
        exclude = ()

    category = forms.ModelChoiceField(queryset=Category.objects.\
            filter(parent__parent__parent__isnull=True).\
            filter(parent__isnull=False).filter(parent__parent__isnull=False))