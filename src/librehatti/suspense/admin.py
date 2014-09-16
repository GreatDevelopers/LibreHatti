from django.contrib import admin
from django.contrib.auth.admin import *
from librehatti.suspense.models import SuspenseOrder, Staff, Department
from librehatti.catalog.actions import mark_inactive, mark_active
from librehatti.catalog.models import *
from librehatti.suspense.forms import StaffForm


admin.autodiscover()

admin.site.register(Department)

class SuspenseOrderAdmin(admin.ModelAdmin):
    exclude=('is_active',)
    list_display = ['id','buyer','delivery_address','date_time','is_active']
    model = SuspenseOrder
    actions = [mark_active, mark_inactive] 
    list_filter = ['purchase_order__date_time']
    search_fields = ['id']
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
    form = StaffForm
    model = Staff
    list_display = ['name', 'department','position', 'daily_income', 'lab']
    list_per_page = 20

admin.site.register(Staff,StaffAdmin) 
admin.site.register(SuspenseOrder,SuspenseOrderAdmin) 
