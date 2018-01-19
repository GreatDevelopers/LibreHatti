"""
urls of catalog are..
"""
#from django.conf.urls import url, patterns
from django.conf.urls import url
from . import views as catalog_views
from django.views.generic import TemplateView
from . import request_change

"""
urls showing the list of item purchased and redirects to page of adding 
new categories of product 
"""
urlpatterns = [
    url(r'^$', catalog_views.index),
    url(r'^select_sub_category/', catalog_views.select_sub_category),
    url(r'^jsreverse/', catalog_views.jsreverse, name = 'jsreverse'),
    url(r'^select_item/', catalog_views.select_item), 
    url(r'^bill_cal/',catalog_views.bill_cal),
    url(r'^list_products/',catalog_views.list_products),
    url(r'^previous_value/',catalog_views.previous_value),
    url(r'^order_added_success/',catalog_views.order_added_success),
    url(r'^change_request/',catalog_views.change_request),
    url(r'^price_per_unit/',catalog_views.price_per_unit),
    url(r'^select_type/',catalog_views.select_type),
    url(r'^nonpaymentorderofsession/',catalog_views.nonpaymentorderofsession),
    url(r'^nonpaymentordersuccess/',catalog_views.nonpaymentordersuccess),
]


urlpatterns += [
   url(r'^request_save/',request_change.request_save, name = 'request_save'),
   url(r'^list_requests/',request_change.list_request),
   url(r'^view_request/',request_change.view_request),
   url(r'^accept_request/',request_change.accept_request),
   url(r'^reject_request/',request_change.reject_request),
   url(r'^permission_denied/',request_change.permission_denied),
]
