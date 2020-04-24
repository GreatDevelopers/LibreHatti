# -*- coding: utf-8 -*-
from django.contrib.auth.admin import admin
from librehatti.catalog.actions import mark_active, mark_inactive
from librehatti.suspense.forms import StaffForm
from librehatti.suspense.models import (
    Department,
    Staff,
    StaffPosition,
    SuspenseOrder,
    Transport,
    Vehicle,
)


admin.autodiscover()

admin.site.register(Department)
admin.site.register(Transport)
admin.site.register(Vehicle)


class SuspenseOrderAdmin(admin.ModelAdmin):
    """
    Admin classes for Suspense Order.
    """

    exclude = ("is_active",)
    list_display = ["id", "buyer", "delivery_address", "date_time", "is_active"]
    model = SuspenseOrder
    actions = [mark_active, mark_inactive]
    list_filter = ["purchase_order__date_time"]
    search_fields = ["id"]
    list_per_page = 20

    def buyer(self, instance):
        return instance.purchase_order.buyer

    def delivery_address(self, instance):
        return instance.purchase_order.delivery_address

    def date_time(self, instance):
        return instance.purchase_order.date_time

    def is_active(self, instance):
        return instance.purchase_order.is_active


class StaffAdmin(admin.ModelAdmin):
    """
    Admin class for staff handling.
    """

    form = StaffForm
    model = Staff
    list_filter = ["department", "position", "lab"]
    list_display = [
        "code",
        "name",
        "department",
        "position",
        "seniority_credits",
        "always_included",
        "daily_ta_da",
        "lab",
    ]
    list_per_page = 20
    search_fields = ["name"]


class StaffPositionAdmin(admin.ModelAdmin):
    """
    Admin section for handling of position of staff.
    """

    model = StaffPosition
    list_display = ["position", "rank"]


admin.site.register(Staff, StaffAdmin)
admin.site.register(StaffPosition, StaffPositionAdmin)
admin.site.register(SuspenseOrder, SuspenseOrderAdmin)
