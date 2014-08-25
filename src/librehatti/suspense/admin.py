from django.contrib import admin
from django.contrib.auth.admin import *
from librehatti.suspense.models import SuspenseOrder, Staff, Department
from librehatti.catalog.actions import mark_inactive, mark_active


admin.autodiscover()
admin.site.register(SuspenseOrder)
admin.site.register(Staff)
admin.site.register(Department)


class SuspenseOrderAdmin(admin.ModelAdmin):
    exclude=('PurchaseOrder.is_active',)
    list_display = ['id','PurchaseOrder.buyer','PurchaseOrder.delivery_address',
                    'PurchaseOrder.date_time','PurchaseOrder.is_active']
    model = SuspenseOrder
    actions = [mark_active, mark_inactive] 
    list_filter = ['PurchaseOrder.date_time']
    search_fields = ['id']
    list_per_page = 20 
