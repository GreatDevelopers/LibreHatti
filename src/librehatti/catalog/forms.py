"""
Forms of catalog are ..
"""
from django import forms

from librehatti.catalog.models import Category
from librehatti.catalog.models import Product
from librehatti.catalog.models import PurchasedItem
from librehatti.catalog.models import PurchaseOrder

import itertools

from ajax_select import make_ajax_field

"""
This form allows user to fill the category name of product
"""
class AddCategory(forms.Form):
    """
    used by catalog views to specify name and different categories used.
    """
    category_name = forms.CharField(max_length=256)
    categories = forms.ModelChoiceField(queryset=Category.objects.all())


class TransportForm1(forms.Form):
    vehicle_id = forms.CharField(max_length=20)
    job_id = forms.IntegerField()
    kilometer = forms.IntegerField()
    rate = forms.IntegerField(initial=10)  
    date = forms.DateField()


class TransportForm2(forms.Form):    
    kilometer = forms.IntegerField()
    date = forms.DateField()  

"""
This form lets user to select item after categories are filtered in dropdown.
"""
class ItemSelectForm(forms.ModelForm):
    class Media:
        js = (
            'js/CategoryDropDown.js',
        )

    try:
        category = forms.ModelChoiceField(queryset=Category.objects.\
     	    filter(parent__isnull=True))
    except:
        pass
    
    product = forms.ModelChoiceField(queryset = Product.objects.all())
     
    def __init__(self, *args, **kwargs):
         super(ItemSelectForm, self).__init__(*args, **kwargs)
         self.fields['category'].widget.attrs={'data-extratype': 'categorydropdown'}
         self.fields['product'].widget.attrs={'data-extratype': 'productdropdown'}

class BuyerForm(forms.ModelForm):
    buyer = make_ajax_field(PurchaseOrder, 'buyer', 'buyer')

    class Meta:
        model = PurchaseOrder
        exclude = ('is_active',)

    class Media:
        js = ('js/hide_add_buyer.js',)

