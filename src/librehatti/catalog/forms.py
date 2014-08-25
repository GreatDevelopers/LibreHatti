"""
Forms of catalog are ..
"""
from django import forms
from librehatti.catalog.models import Category

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
