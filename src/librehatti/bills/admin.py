from django.contrib import admin
from librehatti.bills.models import QuotedItem
from librehatti.bills.models import QuotedOrder
from librehatti.catalog.actions import mark_cancel


class QuotedItemInline(admin.StackedInline):
    model = QuotedItem
    fields = ['quote_item', 'quote_qty', 'quote_discount']
    extra = 10


class QuotedOrderAdmin(admin.ModelAdmin):
    exclude=('is_canceled',)
    list_display = ['id','quote_buyer_id','quote_delivery_address','quote_date_time','is_canceled']
    inlines = [QuotedItemInline]
    model = QuotedOrder
    actions = [mark_cancel]
    list_filter = ['quote_date_time']
    search_fields = ['id']
    list_per_page = 20 
    

admin.site.register(QuotedOrder, QuotedOrderAdmin)
