"""
%% actions.py %%
This file contains the user defined actions for admin site.
"""

from librehatti.catalog.models import *
from django.contrib import admin
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType

"""
Function to mark orders as active.
"""
def mark_active(modeladmin, request, queryset):
    rows_updated = queryset.update(is_active = True)
    if rows_updated == 1:
        message_bit = "1 order is "
    else:
        message_bit = "%s orders are" % rows_updated
    modeladmin.message_user(request, "%s successfully activated" % message_bit)
    content = ContentType.objects.get_for_model(queryset.model)
    for obj in queryset:
        LogEntry.objects.log_action(user_id=request.user.id, 
        content_type_id=content.pk,object_id=obj.pk,action_flag=CHANGE,
        object_repr = "Order Activated",change_message="")

"""
Function to mark orders as inactive/cancelled.
"""
def mark_inactive(modeladmin, request, queryset):
    rows_updated = queryset.update(is_active = False)
    if rows_updated == 1:
        message_bit = "1 order is "
    else:
        message_bit = "%s orders are" % rows_updated
    modeladmin.message_user(request, "%s successfully canceled." % message_bit)
    content = ContentType.objects.get_for_model(queryset.model)
    for obj in queryset:
        LogEntry.objects.log_action(user_id=request.user.id, 
        content_type_id=content.pk,object_id=obj.pk,action_flag=CHANGE,
        object_repr = "Order Canceled",change_message="")


