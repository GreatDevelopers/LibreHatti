"""
urls of catalog are..
"""
#from django.urls import url, patterns
from django.urls import re_path
from . import views as catalog_views
from django.views.generic import TemplateView
from . import request_change

"""
urls showing the list of item purchased and redirects to page of adding 
new categories of product 
"""
urlpatterns = [
    re_path(r'^$', catalog_views.index),
    re_path(r'^select_sub_category/', catalog_views.select_sub_category),
    re_path(r'^jsreverse/', catalog_views.jsreverse, name = 'jsreverse'),
    re_path(r'^select_item/', catalog_views.select_item), 
    re_path(r'^bill_cal/',catalog_views.bill_cal),
    re_path(r'^list_products/',catalog_views.list_products),
    re_path(r'^previous_value/',catalog_views.previous_value),
    re_path(r'^order_added_success/',catalog_views.order_added_success),
    re_path(r'^change_request/',catalog_views.change_request),
    re_path(r'^price_per_unit/',catalog_views.price_per_unit),
    re_path(r'^select_type/',catalog_views.select_type),
    re_path(r'^nonpaymentorderofsession/',catalog_views.nonpaymentorderofsession),
    re_path(r'^nonpaymentordersuccess/',catalog_views.nonpaymentordersuccess),
]


urlpatterns += [
   re_path(r'^request_save/',request_change.request_save, name = 'request_save'),
   re_path(r'^list_requests/',request_change.list_request),
   re_path(r'^view_request/',request_change.view_request),
   re_path(r'^accept_request/',request_change.accept_request),
   re_path(r'^reject_request/',request_change.reject_request),
   re_path(r'^permission_denied/',request_change.permission_denied),
]
