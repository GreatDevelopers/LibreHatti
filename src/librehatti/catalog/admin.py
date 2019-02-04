"""
%% admin.py %%
This file display usage information that admin requires to edit or add 
in database tables, classes in admin interface. This make the data entry
easy as one need to do it through MySQL server.
"""
from librehatti.catalog.models import *

from django.contrib import admin
from django.contrib.auth.admin import *
from django.contrib.admin.models import LogEntry

from librehatti.catalog.forms import ItemSelectForm, BuyerForm
from librehatti.catalog.forms import SpecialCategoriesForm
from librehatti.catalog.actions import mark_inactive, mark_active 

from django.urls import reverse

from ajax_select.admin import AjaxSelectAdmin

from tinymce.widgets import TinyMCE

from django.http import HttpResponse

admin.autodiscover()
admin.site.register(Attributes)
admin.site.register(Catalog)
admin.site.register(Surcharge)
admin.site.register(ModeOfPayment)

def duplicate_event(modeladmin, request, queryset):
    """
    This action is to create a duplicate record
    """
    for object in queryset:
        object.id = None
        object.save()
duplicate_event.short_description = "Duplicate selected record"


class LogEntryAdmin(admin.ModelAdmin):
    """
    This class is used to see logs in a detailed format. It is far much
    better than django recent actions widget.
    """
    model = LogEntry
    list_display = ['id','user','object_repr','content_type','action_time']
    list_filter = ['action_time']
    search_fields = ['object_repr']
    list_per_page = 20


class CatalogInline(admin.TabularInline):
    """
    This class is used to add, edit or delete the attribute and value of 
    item along with inheriting the fields of Procduct class i.e. name, 
    category, price_per_unit and organisation with which user deals
    """
    model = Catalog
    fields = ['attribute', 'value']
    extra = 10


class ProductAdmin(admin.ModelAdmin):
    """
    This class is used to add, edit or delete the details of product along  
    with describing the organisation name and its type from where we are
    purchasing or testing
    """
    fields = ['name', 'category', 'price_per_unit', 'organisation']
    list_display = ['id', 'name', 'category', 'price_per_unit']
    inlines = [CatalogInline]
    actions = [duplicate_event]
    search_fields = ['name']
    list_filter = ['category']
    

class PurchasedItemInline(admin.StackedInline):
    """
    This class is used to add, edit or delete the details of item purchased 
    """
    form = ItemSelectForm
    model = PurchasedItem
    fields = ['type','parent_category', 'sub_category', 'item','price_per_unit', 'qty', ]
    extra = 3


class PurchaseOrderAdmin(AjaxSelectAdmin):
    """
    This class is used to add, edit or delete the details of items 
    purchased but buyer has not confirmed the items purchased, this class
    inherits the fields of PurchaseOrder derscribing the delivery address of
    buyer , is_debit , total discount , tds and mode of payment
    """
    form = BuyerForm
    exclude=('is_active',)
    list_display = ['id','buyer_name','delivery_address','date_time','is_active']
    inlines = [PurchasedItemInline]
    model = PurchaseOrder
    actions = [mark_active, mark_inactive] 
    list_filter = ['date_time']
    search_fields = ['id']
    list_per_page = 20 
    def buyer_name(self, instance):
        return "%s" % (instance.buyer.first_name + ' ' + instance.buyer.\
            last_name + ' ' + instance.buyer.customer.title)

    def response_add(self, request, obj, post_url_continue=None):
        request.session['old_post'] = request.POST
        request.session['purchase_order_id'] = obj.id
        return HttpResponseRedirect(reverse\
            ("librehatti.voucher.views.voucher_generate"))

    def response_change(self, request, obj, post_url_continue=None):
        request.session['old_post'] = request.POST
        request.session['purchase_order_id'] = obj.id
        return HttpResponseRedirect(reverse\
            ("catalog:previous_value"))


class HeaderAdmin(admin.ModelAdmin):
    """
    This class is used to add, edit or delete Header and Footer to be used
    for Bills in the organisation
    """
    Model = HeaderFooter
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in ('header'):
            return db_field.formfield(widget=TinyMCE(
                attrs={'cols': 120, 'rows': 10},
                mce_attrs={'external_link_list_url': reverse\
                ('tinymce.views.flatpages_link_list')},
            ))
        if db_field.name in ('footer'):
            return db_field.formfield(widget=TinyMCE(
                attrs={'cols': 120, 'rows': 10},
                mce_attrs={'external_link_list_url': reverse\
                ('tinymce.views.flatpages_link_list')},
            ))
        return super(HeaderAdmin, self).\
        formfield_for_dbfield(db_field, **kwargs)


class CategoryAdmin(admin.ModelAdmin):

    """
    This class is used to add, edit or delete the details of categories along  
    with describing the organisation name and its type from where we are
    purchasing or testing
    """
    list_display = ['id', 'name', 'parent','unit']
    search_fields = ['name']
    actions = [duplicate_event]
    list_filter = ['parent']
    list_per_page = 20


class NonPaymentOrderAdmin(AjaxSelectAdmin):
    """
    Class for adding Non-Payement orders
    """
    form = BuyerForm
    list_display = ['reference','reference_date', 'date', 'delivery_address', 'item_type']

    def response_add(self, request, obj, post_url_continue=None):
        request.session['old_post'] = request.POST
        request.session['nonpaymentorder_id'] = obj.id
        return HttpResponseRedirect(reverse\
            ("catalog:nonpaymentorderofsession"))

    def response_change(self, request, obj, post_url_continue=None):
        request.session['old_post'] = request.POST
        request.session['purchase_order_id'] = obj.id
        return HttpResponseRedirect(reverse\
            ("catalog:nonpaymentorderofsession"))


class SpecialCategoriesAdmin(admin.ModelAdmin):

    """
    This class is for some special categories on which no 
    taxes are appliable and where no vouchers are generated
    """ 
    model = SpecialCategories
    form = SpecialCategoriesForm
    list_display = ['category', 'voucher', 'tax']

admin.site.register(Category, CategoryAdmin)
admin.site.register(HeaderFooter, HeaderAdmin)
admin.site.register(PurchaseOrder, PurchaseOrderAdmin)
admin.site.register(Product, ProductAdmin) 
admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(NonPaymentOrder, NonPaymentOrderAdmin)
admin.site.register(Unit)
admin.site.register(SpecialCategories, SpecialCategoriesAdmin)
