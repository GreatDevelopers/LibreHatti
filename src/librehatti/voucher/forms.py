# -*- coding: utf-8 -*-
from django import forms
from librehatti.catalog.models import Category
from librehatti.config import _PARENT_CATEGORY, _SUB_CATEGORY
from librehatti.voucher.models import Distribution


class AssignDistributionForm(forms.ModelForm):
    """
    This form lets user to select material after parent categories
    are filtered in dropdown and then distribution type of that material
    can be added.
    """

    class Media:
        js = ("js/distribution_category_select.js",)

    try:
        parent_category = forms.ModelChoiceField(
            queryset=Category.objects.filter(
                parent__parent__isnull=True
            ).filter(parent__isnull=False),
            label=_PARENT_CATEGORY,
        )
        category = forms.ModelChoiceField(
            queryset=Category.objects.all(), label=_SUB_CATEGORY
        )
        distribution = forms.ModelChoiceField(
            queryset=Distribution.objects.all()
        )
    except BaseException:
        pass

    def __init__(self, *args, **kwargs):
        super(AssignDistributionForm, self).__init__(*args, **kwargs)
        self.fields["parent_category"].widget.attrs = {
            "class": "parent_category"
        }
        self.fields["category"].widget.attrs = {"class": "category"}
