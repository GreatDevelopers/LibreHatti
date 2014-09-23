from django import forms

from librehatti.catalog.models import Category
from librehatti.voucher.models import CategoryDistributionType
from librehatti.voucher.models import Distribution

class AssignDistributionForm(forms.ModelForm):
    
    class Media:
        js = (
            'js/distribution_category_select.js',
        )

    try:
        parent_category = forms.ModelChoiceField(queryset=Category.objects.\
     	    filter(parent__parent__isnull=True).filter(parent__isnull=False))
        category = forms.ModelChoiceField(queryset = Category.objects.all())
        distribution = forms.ModelChoiceField(queryset = Distribution.objects.all())
    except:
        pass

    def __init__(self, *args, **kwargs):
         super(AssignDistributionForm, self).__init__(*args, **kwargs)
         self.fields['parent_category'].widget.attrs={'class': 'parent_category'}
         self.fields['category'].widget.attrs={'class': 'category'}