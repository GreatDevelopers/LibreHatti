from django.contrib import admin
from authentication.models import *
from django.contrib.auth.admin import UserAdmin

admin.site.register(AdminOrganisations)
admin.site.register(Address)
admin.site.register(OrganisationType)
admin.site.register(Customer)
admin.site.unregister(User)


class AddressInline(admin.StackedInline):
    model = Address


class CustomerInline(admin.StackedInline):
    model = Customer


class CustomUserAdd(UserAdmin):
    add_fieldsets = (
        ('Add Customer', {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 
            'password1', 'password2')}
        ),
    )
    inlines = [CustomerInline]


admin.site.register(User,CustomUserAdd)

