# -*- coding: utf-8 -*-

from ajax_select import make_ajax_field
from django import forms
from librehatti.bills.models import NoteLine, QuotedOrder
from librehatti.catalog.models import Category, Product
from librehatti.config import ITEM, PARENT_CATEGORY, SUB_CATEGORY, TYPE


class BuyerForm(forms.ModelForm):
    """
    Buyer form for quoted order.
    """

    buyer = make_ajax_field(QuotedOrder, "buyer", "buyer")

    class Meta:
        model = QuotedOrder
        exclude = ("is_active",)

    class Media:
        js = ("js/hide_add_buyer.js", "js/cheque_dd_date.js")


class ItemSelectForm(forms.ModelForm):
    """
    This form lets user to select item after categories are
    filtered in dropdown.
    """

    class Media:
        js = ("js/quote_ajax.js", "js/quoted_price_per_unit.js")

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
        self.fields["price_per_unit"].widget.attrs = {
            "class": "quoted_price_per_unit"
        }


class SelectNoteForm(forms.Form):
    """
    Form for selection of note line while adding note line.
    """

    quoted_order = forms.CharField(
        widget=forms.TextInput(attrs={"readonly": "readonly"})
    )
    note_line = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={"class": "note_checkbox"}),
        queryset=NoteLine.objects.filter(is_permanent=0),
    )
