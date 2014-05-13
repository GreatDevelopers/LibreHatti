from librehatti.catalog.models import *
from django.contrib import admin
from django.contrib.auth.admin import *

admin.autodiscover()
admin.site.register(category)
admin.site.register(attributes)
admin.site.register(catalog)
admin.site.register(admin_organisations)
admin.site.register(address)
admin.site.register(organisation_type)
admin.site.register(customer)
admin.site.unregister(User)

class CatalogInline(admin.TabularInline):
	model = catalog
	fields = ['attribute','value']
	extra = 10

class ProductAdmin(admin.ModelAdmin):
    fields = ['name','category','price','organisation']
    inlines = [CatalogInline] 

class AddressInline(admin.StackedInline):
     model = address

class CustomerInline(admin.StackedInline):
	model = customer

class customUserAdd(UserAdmin):
    add_fieldsets = (
        ('Add Customer', {
            'classes': ('wide',),
            'fields': ('username', 'email','first_name','last_name', 'password1', 'password2')}
        ),
    )
    inlines = [CustomerInline]

class PurchasedItemInline(admin.StackedInline):
	model = purchased_item
	fields = ['item','price','discount','organisation']
	extra = 10

class PurchaseOrderAdmin(admin.ModelAdmin):
	inlines = [PurchasedItemInline]
	

admin.site.register(purchase_order, PurchaseOrderAdmin)
admin.site.register(User,customUserAdd)
admin.site.register(product, ProductAdmin) 

