# -*- coding: utf-8 -*-
"""
Forms of catalog are ..
"""

from ajax_select import make_ajax_field
from django import forms
from librehatti.catalog.models import (
    Category,
    Product,
    PurchaseOrder,
    SpecialCategories,
)
from librehatti.config import ITEM, PARENT_CATEGORY, SUB_CATEGORY, TYPE
from librehatti.voucher.models import FinancialSession


class AddCategory(forms.Form):
    """
    This form allows user to fill the category name of product
    """

    category_name = forms.CharField(max_length=256)
    categories = forms.ModelChoiceField(queryset=Category.objects.all())


class ItemSelectForm(forms.ModelForm):
    """
    This form lets user to select item after categories
    are filtered in dropdown.
    """

    class Media:
        js = ("js/ajax.js", "js/price_per_unit.js")

    try:
        parent_category = forms.ModelChoiceField(
            queryset=Category.objects.filter(
                parent__parent__isnull=True
            ).filter(parent__isnull=False),
            label=PARENT_CATEGORY,
        )
        sub_category = forms.ModelChoiceField(
            queryset=Category.objects.all(), label=SUB_CATEGORY
        )
    except BaseException:
        pass

    item = forms.ModelChoiceField(queryset=Product.objects.all(), label=ITEM)
    CHOICES = (
        ("", "---------"),
        ("1", "Lab Work"),
        ("2", "Field Work"),
        ("3", "Other Services"),
    )
    type = forms.ChoiceField(choices=CHOICES, label=TYPE)
    price_per_unit = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(ItemSelectForm, self).__init__(*args, **kwargs)
        self.fields["type"].widget.attrs = {"class": "type"}
        self.fields["parent_category"].widget.attrs = {
            "class": "parent_category"
        }
        self.fields["sub_category"].widget.attrs = {"class": "sub_category"}
        self.fields["item"].widget.attrs = {"class": "item"}
        self.fields["price_per_unit"].widget.attrs = {"class": "price_per_unit"}


class BuyerForm(forms.ModelForm):

    """
    This form enables the admin to select a user for a purchase purchase_order
    """

    buyer = make_ajax_field(PurchaseOrder, "buyer", "buyer")

    class Meta:
        model = PurchaseOrder
        exclude = ("is_active",)

    class Media:
        js = ("js/hide_add_buyer.js", "js/cheque_dd_date.js")


class ChangeRequestForm(forms.Form):
    """
    This form enables the user to select a purchase order to request
    a change in the Bill Amount
    """

    session = forms.ModelChoiceField(queryset=FinancialSession.objects.all())
    purchase_order = forms.CharField(max_length=10)

    def __init__(self, *args, **kwargs):
        super(ChangeRequestForm, self).__init__(*args, **kwargs)
        self.fields["purchase_order"].widget.attrs = {"class": "form-control"}
        self.fields["session"].widget.attrs = {
            "class": "btn btn-default dropdown-toggle"
        }


class SpecialCategoriesForm(forms.ModelForm):

    """
    This form is used to add special categories by Admin
    """

    class Meta:
        model = SpecialCategories
        exclude = ()

    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(parent__parent__parent__isnull=True)
        .filter(parent__isnull=False)
        .filter(parent__parent__isnull=False)
    )


class ProductListForm(forms.Form):
    """
    This form lets user to select item after categories
    are filtered in dropdown.
    """

    select_lab = forms.ModelChoiceField(
        queryset=Category.objects.filter(parent__isnull=True)
    )
