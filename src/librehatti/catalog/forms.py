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
            'http://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js',
            'js/ajax.js',
        )

    try:
        parent_category = forms.ModelChoiceField(queryset=Category.objects.\
     	    filter(parent__parent__isnull=True).filter(parent__isnull=False))

        sub_category_id = Category.objects.values_list('id',flat=True)
        sub_category_name = Category.objects.values_list('name',flat=True)
        sub_category_choices = [('', '--------')] + [(id, name) for id, name in itertools.\
        izip(sub_category_id, sub_category_name)]
        sub_category = forms.ModelChoiceField(queryset = Category.objects.all())
    except:
        pass

    item = forms.ModelChoiceField(queryset = Product.objects.all())

    def __init__(self, *args, **kwargs):
         super(ItemSelectForm, self).__init__(*args, **kwargs)
         self.fields['parent_category'].widget.attrs={'class': 'parent_category'}
         self.fields['sub_category'].widget.attrs={'class': 'sub_category'}
         self.fields['item'].widget.attrs={'class': 'item'}

class BuyerForm(forms.ModelForm):
    buyer = make_ajax_field(PurchaseOrder, 'buyer', 'buyer')

    class Meta:
        model = PurchaseOrder
        exclude = ('is_active',)

    class Media:
        js = ('js/hide_add_buyer.js',)

