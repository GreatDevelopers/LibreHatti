from django.contrib import admin
from librehatti.bills.models import *
from django.contrib.auth.admin import *
from librehatti.bills.forms import ItemSelectForm
from librehatti.catalog.actions import mark_inactive, mark_active
from django.http import HttpResponse,HttpResponseRedirect
admin.autodiscover() 


class QuotedItemInline(admin.StackedInline):
    model = QuotedItem
    form = ItemSelectForm
    fields = ['parent_category', 'sub_category','item','qty']
    extra = 10


class QuotedOrderAdmin(admin.ModelAdmin):
    exclude=('is_active',)
    list_display = ['id','buyer_id','delivery_address','organisation',
                    'total_discount','tds','mode_of_payment','confirm_status']
    inlines = [QuotedItemInline]
    model = QuotedOrder
    actions = [mark_active, mark_inactive] 
    list_filter = ['date_time']
    search_fields = ['id']
    list_per_page = 20 
    def response_add(self, request, obj, post_url_continue=None):
        request.session['old_post'] = request.POST
        request.session['quote_order_id'] = obj.id
	return HttpResponseRedirect('/bills/bill_cal')
        

   

admin.site.register(QuotedOrder, QuotedOrderAdmin)
