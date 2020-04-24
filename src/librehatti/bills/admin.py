# -*- coding: utf-8 -*-

from django.contrib.auth.admin import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from librehatti.bills.forms import BuyerForm, ItemSelectForm
from librehatti.bills.models import NoteLine, QuotedItem, QuotedOrder
from librehatti.catalog.actions import mark_active, mark_inactive


admin.autodiscover()


class QuotedItemInline(admin.StackedInline):
    """
    This class is used to add, edit or delete the details of item purchased.
    """

    model = QuotedItem
    form = ItemSelectForm
    fields = [
        "type",
        "parent_category",
        "sub_category",
        "item",
        "price_per_unit",
        "qty",
    ]
    extra = 2


class QuotedOrderAdmin(admin.ModelAdmin):
    """
    This class is used to add, edit or delete the details of items
    purchased but buyer has not confirmed the items purchased, this class
    inherits the fields of PurchaseOrder derscribing the delivery address of
    buyer , is_debit , total discount , tds and mode of payment
    """

    form = BuyerForm
    exclude = ("is_active",)
    list_display = [
        "id",
        "buyer_name",
        "delivery_address",
        "date_time",
        "is_active",
    ]
    inlines = [QuotedItemInline]
    model = QuotedOrder
    actions = [mark_active, mark_inactive]
    list_filter = ["date_time"]
    search_fields = ["id"]
    list_per_page = 20

    def buyer_name(self, instance):
        return "%s" % (
            instance.buyer.first_name
            + " "
            + instance.buyer.last_name
            + " "
            + instance.buyer.customer.title
        )

    def response_add(self, request, obj, post_url_continue=None):
        request.session["old_post"] = request.POST
        request.session["quoted_order_id"] = obj.id
        return HttpResponseRedirect(reverse("bills:quoted_order_of_session"))


class NoteLineAdmin(admin.ModelAdmin):
    """
    Handles admin panel of note line.
    Admin can delete add. or make note line permanent.
    """

    Model = NoteLine


admin.site.register(NoteLine, NoteLineAdmin)
admin.site.register(QuotedOrder, QuotedOrderAdmin)
