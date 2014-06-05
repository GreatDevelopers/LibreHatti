from django import forms
from librehatti.catalog.models import *


class addCategory(forms.Form):
        categoryName = forms.CharField(max_length=256)
        categories = forms.ModelChoiceField(queryset=category.objects.all())
