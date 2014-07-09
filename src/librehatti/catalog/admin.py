from librehatti.catalog.models import *
from django.contrib import admin
from django.contrib.auth.admin import *

admin.autodiscover()
admin.site.register(Category)
admin.site.register(Attributes)
admin.site.register(Catalog)
admin.site.register(Surcharge)


class CatalogInline(admin.TabularInline):
    model = Catalog
    fields = ['attribute', 'value']
    extra = 10


class ProductAdmin(admin.ModelAdmin):
    fields = ['name', 'category', 'price_per_unit', 'organisation']
    inlines = [CatalogInline] 


class PurchasedItemInline(admin.StackedInline):
    model = PurchasedItem
    fields = ['item', 'qty', ]
    extra = 10


class PurchaseOrderAdmin(admin.ModelAdmin):
    inlines = [PurchasedItemInline]
	

admin.site.register(PurchaseOrder, PurchaseOrderAdmin)
admin.site.register(Product, ProductAdmin) 

