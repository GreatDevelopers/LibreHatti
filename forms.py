from django import forms
from librehatti.catalog.models import Category


class AddCategory(forms.Form):
    """
    It is used by the views of catalog to specify the name of category and different categories used. 
    """
    category_name = forms.CharField(max_length=256)
    categories = forms.ModelChoiceField(queryset=Category.objects.all())
