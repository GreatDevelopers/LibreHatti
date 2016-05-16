"""
urls of catalog are..
"""
from django.conf.urls import url, patterns

from django.views.generic import TemplateView

from librehatti.catalog import views
from librehatti.catalog import request_change

"""
urls showing the list of item purchased and redirects to page of adding 
new categories of product 
"""
urlpatterns = [
    url(r'^select_sub_category/', views.select_sub_category, name='select_sub_category'),
    url(r'^jsreverse/', views.jsreverse, name='jsreverse'),
    url(r'^select_item/', views.select_item, name='select_item'), 
    url(r'^bill_cal/',views.bill_cal, name='bill_cal'),
    url(r'^list_products/',views.list_products, name='list_products'),
    url(r'^previous_value/',views.previous_value, name='previous_value'),
    url(r'^order_added_success/',views.order_added_success, name='order_added_success'),
    url(r'^change_request/',views.change_request, name='change_request'),
    url(r'^price_per_unit/',views.price_per_unit, name='price_per_unit'),
    url(r'^select_type/',views.select_type, name='select_type'),
    url(r'^nonpaymentorderofsession/',views.nonpaymentorderofsession, name='nonpaymentorderofsession'),
    url(r'^nonpaymentordersuccess/',views.nonpaymentordersuccess, name='nonpaymentordersuccess'),
    url(r'^request_save/',request_change.request_save, name='request_save'),
    url(r'^list_requests/',request_change.list_request, name='list_requests'),
    url(r'^view_request/',request_change.view_request, name='view_request'),
    url(r'^accept_request/',request_change.accept_request, name='accept_request'),
    url(r'^reject_request/',request_change.reject_request, name='reject_request'),
    url(r'^permission_denied/',request_change.permission_denied, name='permission_denied'),
]