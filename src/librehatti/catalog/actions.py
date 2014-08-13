"""
%% actions.py %%
This file contains the user defined actions for admin site.
"""

from librehatti.catalog.models import *
from django.contrib import admin

"""
Function to mark orders as cancel.
"""
def mark_cancel(modeladmin, request, queryset):
    rows_updated = queryset.update(is_canceled = True)
    if rows_updated == 1:
        message_bit = "1 order is "
    else:
        message_bit = "%s orders are" % rows_updated
    modeladmin.message_user(request, "%s successfully canceled." % message_bit)