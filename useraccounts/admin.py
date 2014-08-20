"""
%% admin.py %%
This file display usage information that admin requires to edit or add 
in database tables, classes in admin interface. This make the data entry
easy as one need to do it through MySQL server.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from useraccounts.models import *

"""
these fields are required in admin interface to add the details of 
particular organisation with which the user deals and also customer 
details whether its individual or owner of a company
"""
admin.site.register(AdminOrganisations)
admin.site.register(Address)
admin.site.register(OrganisationType)
admin.site.register(Customer)
admin.site.unregister(User)

"""
This class is used to add, edit or delete the address of the organisation
or user
"""
class AddressInline(admin.StackedInline):
     model = Address

"""
This class is used to add, edit or delete the details of customer 
mentioning the address along with ithe information whether customer is  
org_type or not
"""
class CustomerInline(admin.StackedInline):
     model = Customer

"""
This class is used to add new customer, edit or delete existing 
customers specifying the username , email, first and last name and 
confirming the passwords
"""
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

