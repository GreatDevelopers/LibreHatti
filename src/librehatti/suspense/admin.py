from django.contrib import admin
from librehatti.suspense.models import SuspenseOrder, Staff, Department
from librehatti.catalog.actions import mark_cancel


admin.autodiscover()
admin.site.register(SuspenseOrder)
admin.site.register(Staff)
admin.site.register(Department)

class SuspenseOrderAdmin(admin.ModelAdmin):
    exclude=('PurchaseOrder.is_canceled',)
    list_display = ['id','PurchaseOrder.buyer','PurchaseOrder.delivery_address',
                    'PurchaseOrder.date_time','PurchaseOrderis_canceled']
    model = SuspenseOrder
    actions = [mark_cancel]
    list_filter = ['PurchaseOrder.date_time']
    search_fields = ['id']
    list_per_page = 20 
