"""
Forms of catalog are ..
"""
from django import forms
from librehatti.catalog.models import Category
from librehatti.catalog.models import Product
from librehatti.catalog.models import PurchasedItem
from librehatti.catalog.models import LevelOne
import itertools

"""
This form allows user to fill the category name of product
"""
class AddCategory(forms.Form):
    """
    used by catalog views to specify name and different categories used.
    """
    category_name = forms.CharField(max_length=256)
    categories = forms.ModelChoiceField(queryset=Category.objects.all())

class MaterialSelectForm(forms.ModelForm):
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js',
            'js/ajax.js', 
        )
    lab = forms.ModelChoiceField(queryset=Category.objects.\
     	filter(parent__parent__isnull=True).filter(parent__isnull=False))
     
    mat_id = Category.objects.values_list('id',flat=True)
    mat_name = Category.objects.values_list('name',flat=True)
    mat_choices = [('', '--------')] + [(id, name) for id, name in itertools.\
    izip(mat_id, mat_name)]
    material = forms.ChoiceField(mat_choices)
     
    item_id = Product.objects.values_list('id',flat=True)
    item_name = Product.objects.values_list('name',flat=True)
    item_choices = [('', '--------')] + [(id, name) for id, name in itertools.\
    izip(item_id, item_name)]
    item = forms.ChoiceField(item_choices)
    item = forms.ModelChoiceField(queryset = Product.objects.all())
     
    def __init__(self, *args, **kwargs):
         super(MaterialSelectForm, self).__init__(*args, **kwargs)
         self.fields['lab'].widget.attrs={'class': 'lab'}
         self.fields['material'].widget.attrs={'class': 'material'}
         self.fields['item'].widget.attrs={'class': 'item'}
