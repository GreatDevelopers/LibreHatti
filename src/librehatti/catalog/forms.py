"""
Forms of catalog are ..
"""
from django import forms
from librehatti.catalog.models import Category

"""
This form allows user to fill the category name of product
"""
class AddCategory(forms.Form):
    category_name = forms.CharField(max_length=256)
    categories = forms.ModelChoiceField(queryset=Category.objects.all())
