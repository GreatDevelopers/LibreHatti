"""
Forms of catalog are ..
"""
from django import forms
from librehatti.catalog.models import Category
from librehatti.catalog.models import Product
from librehatti.catalog.models import PurchasedItem
import itertools
from librehatti.catalog.models import Transport

"""
This form allows user to fill the category name of product
"""
class AddCategory(forms.Form):
    """
    used by catalog views to specify name and different categories used.
    """
    category_name = forms.CharField(max_length=256)
    categories = forms.ModelChoiceField(queryset=Category.objects.all())


class TransportFormA(forms.ModelForm):
    class Meta:
        model = Transport
        exclude = ['total']

class TransportFormB(forms.Form):    
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
        sub_category = forms.ChoiceField(sub_category_choices)
    except:
        pass
    
    item = forms.ModelChoiceField(queryset = Product.objects.all())
     
    def __init__(self, *args, **kwargs):
         super(ItemSelectForm, self).__init__(*args, **kwargs)
         self.fields['parent_category'].widget.attrs={'class': 'parent_category'}
         self.fields['sub_category'].widget.attrs={'class': 'sub_category'}
         self.fields['item'].widget.attrs={'class': 'item'}
