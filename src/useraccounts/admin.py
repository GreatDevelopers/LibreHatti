# -*- coding: utf-8 -*-
"""
%% admin.py %%
This file display usage information that admin requires to edit or add
in database tables, classes in admin interface. This make the data entry
easy as one need to do it through MySQL server.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from useraccounts.models import (
    Address,
    AdminOrganisations,
    Customer,
    OrganisationType,
    User,
)


admin.site.register(AdminOrganisations)
admin.site.register(Address)
admin.site.register(OrganisationType)
admin.site.register(Customer)
admin.site.unregister(User)


class AddressInline(admin.StackedInline):
    """
    This class is used to add, edit or delete the address of the organisation
    or user
    """

    model = Address


class CustomerInline(admin.StackedInline):
    """
    This class is used to add, edit or delete the details of customer
    mentioning the address along with ithe information whether customer is
    org_type or not
    """

    model = Customer


class CustomUserAdd(UserAdmin):
    """
    This class is used to add new customer, edit or delete existing
    customers specifying the username , email, first and last name and
    confirming the passwords
    """

    list_display = ["user", "email", "address", "date_joined"]
    add_fieldsets = (
        (
            "Add Customer",
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    inlines = [CustomerInline]

    def user(self, instance):
        return "%s" % (
            instance.first_name
            + " "
            + instance.last_name
            + " "
            + instance.customer.title
        )

    def address(self, instance):
        return "%s" % (
            instance.customer.address.street_address
            + " "
            + instance.customer.address.district
        )


admin.site.register(User, CustomUserAdd)
