from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from useraccounts.models import *

admin.site.register(admin_organisations)
admin.site.register(address)
admin.site.register(organisation_type)
admin.site.register(customer)
admin.site.unregister(User)


class AddressInline(admin.StackedInline):
     model = address


class CustomerInline(admin.StackedInline):
     model = customer


class customUserAdd(UserAdmin):
    add_fieldsets = (
        ('Add Customer', {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 
            'password1', 'password2')}
        ),
    )
    inlines = [CustomerInline]

admin.site.register(User,customUserAdd)

