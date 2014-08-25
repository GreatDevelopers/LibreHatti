from django.contrib import admin
from librehatti.bills.models import *
from django.contrib.auth.admin import *
from librehatti.catalog.actions import mark_inactive, mark_active
admin.autodiscover() 


class QuotedItemInline(admin.StackedInline):
    model = QuotedItem
    fields = ['quote_item', 'quote_qty', 'quote_discount']
    extra = 10


class QuotedOrderAdmin(admin.ModelAdmin):
    exclude=('is_active',)
    list_display = ['id','quote_buyer','quote_delivery_address',
                    'quote_date_time','is_active']
    inlines = [QuotedItemInline]
    model = QuotedOrder
    actions = [mark_active, mark_inactive] 
    list_filter = ['quote_date_time']
    search_fields = ['id']
    list_per_page = 20 
   

admin.site.register(QuotedOrder, QuotedOrderAdmin)
